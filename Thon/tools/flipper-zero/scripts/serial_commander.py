#!/usr/bin/env python3
"""
Flipper Zero Serial Commander
==============================
Auto-detects the Flipper Zero COM port via USB VID/PID, connects via serial,
and provides an interactive command interface.

Supports:
  - Flipper Zero CLI (VID 0483, PID 5740)
  - WiFi Devboard passthrough
  - Auto-detection with fallback to manual port specification

Usage:
  python serial_commander.py                    # Auto-detect and interactive
  python serial_commander.py --detect           # Just detect, don't connect
  python serial_commander.py --port COM4        # Manual port override
  python serial_commander.py --cmd "info"       # One-shot command
  python serial_commander.py --help

Platform: Windows / Python 3.x
"""

import argparse
import sys
import time
import signal
import json
from datetime import datetime, timezone

try:
    import serial
    import serial.tools.list_ports
except ImportError:
    print("ERROR: pyserial not installed. Run: pip install pyserial")
    sys.exit(1)


# Flipper Zero USB identifiers
FLIPPER_VID = 0x0483          # STMicroelectronics
FLIPPER_PID_NORMAL = 0x5740   # Flipper Zero CDC serial
FLIPPER_PID_DFU = 0xDF11      # Flipper Zero DFU mode

# ESP32-S2 WiFi Devboard identifiers
ESP32S2_VID = 0x303A          # Espressif
SPARKFUN_VID = 0x1B4F         # SparkFun (WiFi devboard alternate)

BAUD_RATE = 115200
READ_TIMEOUT = 2.0
WRITE_TIMEOUT = 2.0


class FlipperDetector:
    """Detects Flipper Zero and WiFi devboard on USB/COM ports."""

    @staticmethod
    def scan_ports():
        """Scan all COM ports and classify devices."""
        results = {
            "flipper": None,
            "flipper_dfu": None,
            "wifi_devboard": None,
            "other": [],
            "scan_time": datetime.now(timezone.utc).isoformat(),
        }

        ports = serial.tools.list_ports.comports()
        for port in ports:
            info = {
                "port": port.device,
                "description": port.description,
                "vid": hex(port.vid) if port.vid else None,
                "pid": hex(port.pid) if port.pid else None,
                "serial_number": port.serial_number,
                "manufacturer": port.manufacturer,
                "hwid": port.hwid,
            }

            if port.vid == FLIPPER_VID:
                if port.pid == FLIPPER_PID_NORMAL:
                    results["flipper"] = info
                elif port.pid == FLIPPER_PID_DFU:
                    results["flipper_dfu"] = info
                else:
                    results["other"].append(info)
            elif port.vid in (ESP32S2_VID, SPARKFUN_VID):
                results["wifi_devboard"] = info
            elif port.vid is not None:
                results["other"].append(info)

        return results

    @staticmethod
    def find_flipper_port():
        """Find the Flipper Zero COM port. Returns port name or None."""
        scan = FlipperDetector.scan_ports()

        if scan["flipper"]:
            return scan["flipper"]["port"]

        if scan["flipper_dfu"]:
            print(f"⚠️  Flipper Zero detected in DFU mode on {scan['flipper_dfu']['port']}")
            print("   The device is in firmware update mode — serial CLI unavailable.")
            print("   Try: Unplug USB → wait 5s → replug → ensure normal boot.")
            return None

        return None


class FlipperSerial:
    """Serial connection to Flipper Zero CLI."""

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
                timeout=READ_TIMEOUT,
                write_timeout=WRITE_TIMEOUT,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
            )
            time.sleep(0.5)
            # Flush any pending data
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            print(f"✅ Connected to {self.port} @ {self.baud} baud")
            return True
        except serial.SerialException as e:
            print(f"❌ Failed to connect to {self.port}: {e}")
            return False

    def disconnect(self):
        """Close serial connection cleanly."""
        if self.ser and self.ser.is_open:
            try:
                self.ser.close()
                print(f"🔌 Disconnected from {self.port}")
            except Exception:
                pass

    def send_command(self, cmd, timeout=3.0):
        """Send a command and read the response."""
        if not self.ser or not self.ser.is_open:
            return None

        try:
            # Send command with newline
            self.ser.write(f"{cmd}\r\n".encode("utf-8"))
            self.ser.flush()

            # Read response with timeout
            response_lines = []
            start = time.time()
            while (time.time() - start) < timeout:
                if self.ser.in_waiting:
                    line = self.ser.readline().decode("utf-8", errors="replace").strip()
                    if line:
                        response_lines.append(line)
                    start = time.time()  # Reset timeout on data
                else:
                    time.sleep(0.05)

            return "\n".join(response_lines)
        except serial.SerialException as e:
            print(f"❌ Serial error: {e}")
            return None

    def interactive_mode(self):
        """Run interactive CLI session."""
        print("\n📡 Flipper Zero Interactive CLI")
        print("   Type commands to send to the Flipper.")
        print("   Type 'exit' or 'quit' to disconnect.")
        print("   Type 'help' for Flipper CLI help.")
        print("-" * 50)

        # Set up clean exit on Ctrl+C
        def signal_handler(sig, frame):
            print("\n\n⚡ Ctrl+C detected — disconnecting...")
            self.disconnect()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        while True:
            try:
                cmd = input("\nflipper> ").strip()
            except EOFError:
                break

            if not cmd:
                continue
            if cmd.lower() in ("exit", "quit"):
                break

            response = self.send_command(cmd)
            if response:
                print(response)
            else:
                print("(no response)")

        self.disconnect()


def detect_and_report():
    """Detect all relevant devices and report."""
    print("🔍 Scanning USB/COM ports for Flipper Zero...\n")
    scan = FlipperDetector.scan_ports()

    if scan["flipper"]:
        f = scan["flipper"]
        print(f"✅ Flipper Zero found: {f['port']}")
        print(f"   VID:PID  = {f['vid']}:{f['pid']}")
        print(f"   Serial   = {f['serial_number']}")
        print(f"   Desc     = {f['description']}")
    elif scan["flipper_dfu"]:
        d = scan["flipper_dfu"]
        print(f"⚠️  Flipper Zero in DFU mode: {d['port'] if d.get('port') else 'N/A'}")
        print(f"   VID:PID  = {d['vid']}:{d['pid']}")
        print(f"   Serial   = {d['serial_number']}")
        print("   ⚡ Device is in firmware update mode — not ready for serial CLI")
    else:
        print("❌ Flipper Zero not detected on any COM port.")
        print("   Ensure the Flipper is connected via USB and powered on.")

    if scan["wifi_devboard"]:
        w = scan["wifi_devboard"]
        print(f"\n📶 WiFi Devboard found: {w['port']}")
        print(f"   VID:PID  = {w['vid']}:{w['pid']}")
        print(f"   Serial   = {w['serial_number']}")
    else:
        print("\n📶 WiFi Devboard: not detected as separate device")
        print("   (may be accessible via Flipper passthrough)")

    if scan["other"]:
        print(f"\n📋 Other serial devices: {len(scan['other'])}")
        for o in scan["other"]:
            print(f"   {o['port']}: {o['description']} ({o['vid']}:{o['pid']})")

    # Return raw scan data
    return scan


def main():
    parser = argparse.ArgumentParser(
        description="Flipper Zero Serial Commander — auto-detect and interact with Flipper Zero CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                       Auto-detect and start interactive CLI
  %(prog)s --detect              Detect devices only (no connection)
  %(prog)s --port COM4           Use specific port
  %(prog)s --cmd "info"          Send one-shot command
  %(prog)s --cmd "info" --json   Output response as JSON
        """,
    )
    parser.add_argument("--detect", action="store_true", help="Detect devices only, don't connect")
    parser.add_argument("--port", type=str, help="Manual COM port override (e.g. COM4)")
    parser.add_argument("--cmd", type=str, help="Send a single command and exit")
    parser.add_argument("--baud", type=int, default=BAUD_RATE, help=f"Baud rate (default: {BAUD_RATE})")
    parser.add_argument("--json", action="store_true", help="Output in JSON format (with --detect or --cmd)")
    parser.add_argument("--timeout", type=float, default=3.0, help="Command response timeout in seconds")

    args = parser.parse_args()

    # Detection mode
    if args.detect:
        scan = detect_and_report()
        if args.json:
            print(f"\n{json.dumps(scan, indent=2)}")
        sys.exit(0 if scan["flipper"] else 1)

    # Find port
    port = args.port
    if not port:
        port = FlipperDetector.find_flipper_port()
        if not port:
            detect_and_report()
            sys.exit(1)
        print(f"🎯 Auto-detected Flipper on {port}")

    # Connect
    flipper = FlipperSerial(port, args.baud)
    if not flipper.connect():
        sys.exit(1)

    try:
        if args.cmd:
            # One-shot command mode
            response = flipper.send_command(args.cmd, timeout=args.timeout)
            if args.json:
                print(json.dumps({"command": args.cmd, "response": response}))
            else:
                print(response if response else "(no response)")
        else:
            # Interactive mode
            flipper.interactive_mode()
    finally:
        flipper.disconnect()


if __name__ == "__main__":
    main()
