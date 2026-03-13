#!/usr/bin/env python3
"""
Flipper Zero Device Snapshot
===============================
Pulls complete device state from the Flipper Zero and saves a structured
snapshot to the configs/ directory with ISO-8601 timestamps.

Queries:
  - Firmware version and build info
  - Hardware revision
  - SD card state and storage info
  - WiFi devboard status (if present)
  - Installed apps
  - Power state and battery level

Usage:
  python device_snapshot.py                    # Auto-detect, snapshot, save
  python device_snapshot.py --port COM4        # Manual port
  python device_snapshot.py --output configs/  # Custom output dir
  python device_snapshot.py --print            # Print to stdout only

Platform: Windows / Python 3.x
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone

try:
    import serial
    import serial.tools.list_ports
except ImportError:
    print("ERROR: pyserial not installed. Run: pip install pyserial")
    sys.exit(1)


FLIPPER_VID = 0x0483
FLIPPER_PID_NORMAL = 0x5740
FLIPPER_PID_DFU = 0xDF11
BAUD_RATE = 115200

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIGS_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "configs")


def find_flipper_port():
    """Auto-detect Flipper Zero COM port."""
    for port in serial.tools.list_ports.comports():
        if port.vid == FLIPPER_VID and port.pid == FLIPPER_PID_NORMAL:
            return port.device
    # Check DFU mode
    for port in serial.tools.list_ports.comports():
        if port.vid == FLIPPER_VID and port.pid == FLIPPER_PID_DFU:
            print(f"⚠️  Flipper in DFU mode — snapshot unavailable")
            return None
    return None


class DeviceSnapshot:
    """Captures full device state from Flipper Zero."""

    # CLI commands to query device state (Flipper Zero FW 1.4.3+)
    QUERIES = {
        "device_info": "info device",
        "power_info": "info power",
        "storage_internal": "storage info /int",
        "storage_external": "storage info /ext",
        "bt_info": "bt hci_info",
        "gpio_apps": "storage list /ext/apps/GPIO",
    }

    def __init__(self, port, baud=BAUD_RATE):
        self.port = port
        self.baud = baud
        self.ser = None

    def connect(self):
        """Open serial connection."""
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baud,
                timeout=2.0,
                write_timeout=2.0,
            )
            time.sleep(0.5)
            self.ser.reset_input_buffer()
            return True
        except serial.SerialException as e:
            print(f"❌ Connection failed: {e}")
            return False

    def disconnect(self):
        """Close connection."""
        if self.ser and self.ser.is_open:
            self.ser.close()

    def query(self, cmd, timeout=3.0):
        """Send command and collect response."""
        if not self.ser:
            return ""

        self.ser.reset_input_buffer()
        self.ser.write(f"{cmd}\r\n".encode())
        self.ser.flush()

        lines = []
        start = time.time()
        while (time.time() - start) < timeout:
            if self.ser.in_waiting:
                line = self.ser.readline().decode("utf-8", errors="replace").strip()
                if line and line != cmd:  # Filter echo
                    lines.append(line)
                start = time.time()
            else:
                time.sleep(0.05)

        return "\n".join(lines)

    def take_snapshot(self):
        """Query all device information and build structured snapshot."""
        print("📸 Taking device snapshot...\n")

        snapshot = {
            "snapshot_time": datetime.now(timezone.utc).isoformat(),
            "port": self.port,
            "sections": {},
        }

        # USB port metadata
        for port in serial.tools.list_ports.comports():
            if port.device == self.port:
                snapshot["usb"] = {
                    "vid": hex(port.vid) if port.vid else None,
                    "pid": hex(port.pid) if port.pid else None,
                    "serial_number": port.serial_number,
                    "manufacturer": port.manufacturer,
                    "description": port.description,
                }
                break

        # Run each query
        for key, cmd in self.QUERIES.items():
            print(f"   Querying: {cmd}...")
            response = self.query(cmd)
            snapshot["sections"][key] = {
                "command": cmd,
                "response": response,
                "parsed": self._parse_key_value(response),
            }

        # Extract key fields into top-level summary
        snapshot["summary"] = self._build_summary(snapshot["sections"])

        return snapshot

    @staticmethod
    def _parse_key_value(text):
        """Parse 'key : value' pairs from Flipper CLI response."""
        parsed = {}
        for line in text.split("\n"):
            # Flipper uses 'key.sub  : value' format with variable spacing
            if ":" in line and not line.startswith(">"):
                key, _, value = line.partition(":")
                key = key.strip().lower().replace(" ", "_")
                value = value.strip()
                if key and value:
                    parsed[key] = value
        return parsed

    @staticmethod
    def _build_summary(sections):
        """Build a top-level summary from parsed sections."""
        summary = {}

        # All device info comes from 'info device' in FW 1.4.3+
        di = sections.get("device_info", {}).get("parsed", {})
        summary["firmware_version"] = di.get("firmware.version", "unknown")
        summary["firmware_build"] = di.get("firmware.build.date", "unknown")
        summary["firmware_branch"] = di.get("firmware.branch.name", "unknown")
        summary["firmware_origin"] = di.get("firmware.origin.fork", "unknown")
        summary["hardware_model"] = di.get("hardware.model", "unknown")
        summary["hardware_revision"] = di.get("hardware.ver", "unknown")
        summary["hardware_uid"] = di.get("hardware.uid", "unknown")
        summary["hardware_name"] = di.get("hardware.name", "unknown")
        summary["ble_mac"] = di.get("radio.ble.mac", "unknown")
        summary["region"] = di.get("hardware.region.provisioned", "unknown")

        # Power from 'info power'
        pwr = sections.get("power_info", {}).get("parsed", {})
        summary["battery_charge"] = pwr.get("charge.level", "unknown")
        summary["battery_state"] = pwr.get("charge.state", "unknown")
        summary["battery_health"] = pwr.get("battery.health", "unknown")
        summary["battery_temp"] = pwr.get("battery.temp", "unknown")

        # Storage
        ext = sections.get("storage_external", {}).get("parsed", {})
        summary["sd_card_label"] = ext.get("label", "unknown")
        summary["sd_card_type"] = ext.get("type", "unknown")

        return summary


def save_snapshot(snapshot, output_dir):
    """Save snapshot to file."""
    os.makedirs(output_dir, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")
    filepath = os.path.join(output_dir, f"{ts}_device_snapshot.json")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)

    print(f"\n💾 Snapshot saved: {filepath}")
    return filepath


def print_snapshot(snapshot):
    """Print snapshot summary to console."""
    print("\n" + "=" * 60)
    print("  FLIPPER ZERO DEVICE SNAPSHOT")
    print("=" * 60)

    s = snapshot.get("summary", {})
    usb = snapshot.get("usb", {})

    print(f"\n  📅 Captured:        {snapshot['snapshot_time']}")
    print(f"  🔌 Port:            {snapshot['port']}")
    print(f"  🏭 USB VID:PID:     {usb.get('vid', '?')}:{usb.get('pid', '?')}")
    print(f"  🔢 Serial:          {usb.get('serial_number', '?')}")
    print(f"\n  📀 Firmware:         {s.get('firmware_version', '?')}")
    print(f"  🔧 Build:           {s.get('firmware_build', '?')}")
    print(f"  🌿 Branch:          {s.get('firmware_branch', '?')}")
    print(f"\n  🖥️  Hardware:        {s.get('hardware_model', '?')}")
    print(f"  📋 Revision:        {s.get('hardware_revision', '?')}")
    print(f"  🆔 UID:             {s.get('hardware_uid', '?')}")
    print(f"\n  💾 SD Card Total:   {s.get('sd_card_total', '?')}")
    print(f"  💾 SD Card Free:    {s.get('sd_card_free', '?')}")
    print(f"\n  🔋 Battery:         {s.get('battery_charge', '?')}")
    print(f"  ❤️  Health:          {s.get('battery_health', '?')}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Flipper Zero Device Snapshot — capture and save complete device state",
    )
    parser.add_argument("--port", type=str, help="COM port (auto-detect if omitted)")
    parser.add_argument("--output", type=str, default=DEFAULT_CONFIGS_DIR, help="Output directory")
    parser.add_argument("--print", dest="print_only", action="store_true", help="Print to stdout only, don't save")
    parser.add_argument("--baud", type=int, default=BAUD_RATE, help=f"Baud rate (default: {BAUD_RATE})")

    args = parser.parse_args()

    # Find port
    port = args.port
    if not port:
        port = find_flipper_port()
        if not port:
            print("❌ Flipper Zero not detected. Use --port to specify manually.")
            sys.exit(1)
        print(f"🎯 Auto-detected Flipper on {port}")

    # Connect and snapshot
    device = DeviceSnapshot(port, args.baud)
    if not device.connect():
        sys.exit(1)

    try:
        snapshot = device.take_snapshot()
        print_snapshot(snapshot)

        if not args.print_only:
            save_snapshot(snapshot, args.output)
    finally:
        device.disconnect()


if __name__ == "__main__":
    main()
