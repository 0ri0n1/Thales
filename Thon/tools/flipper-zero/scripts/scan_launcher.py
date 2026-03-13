#!/usr/bin/env python3
"""
Flipper Zero WiFi Scan Launcher
=================================
Triggers a WiFi AP scan via the Flipper Zero serial interface (WiFi devboard),
parses results, and saves to captures/ with ISO-8601 timestamped filenames.

Supports both Marauder and stock AT firmware command sets.

Usage:
  python scan_launcher.py                          # Auto-detect, scan, save
  python scan_launcher.py --port COM4              # Manual port
  python scan_launcher.py --duration 15            # Scan for 15 seconds
  python scan_launcher.py --output captures/       # Custom output dir
  python scan_launcher.py --format json            # Output as JSON (default)
  python scan_launcher.py --format csv             # Output as CSV

Platform: Windows / Python 3.x
"""

import argparse
import csv
import io
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


# Device identifiers
FLIPPER_VID = 0x0483
FLIPPER_PID_NORMAL = 0x5740
BAUD_RATE = 115200

# Default paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CAPTURES_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "captures")


def find_flipper_port():
    """Auto-detect Flipper Zero COM port."""
    for port in serial.tools.list_ports.comports():
        if port.vid == FLIPPER_VID and port.pid == FLIPPER_PID_NORMAL:
            return port.device
    return None


def generate_filename(output_dir, fmt="json"):
    """Generate ISO-8601 timestamped filename."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"{ts}_ap_scan.{fmt}"
    return os.path.join(output_dir, filename)


class WiFiScanner:
    """WiFi scanner that communicates with Flipper Zero / WiFi devboard."""

    # Marauder command set
    MARAUDER_COMMANDS = {
        "scan_ap": "scanap",
        "stop_scan": "stopscan",
        "list_ap": "list -a",
        "version": "version",
    }

    # Stock AT firmware command set
    AT_COMMANDS = {
        "scan_ap": "AT+CWLAP",
        "version": "AT+GMR",
    }

    def __init__(self, port, baud=BAUD_RATE):
        self.port = port
        self.baud = baud
        self.ser = None
        self.firmware_type = None

    def connect(self):
        """Open serial connection to the Flipper/WiFi devboard."""
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baud,
                timeout=2.0,
                write_timeout=2.0,
            )
            time.sleep(0.5)
            self.ser.reset_input_buffer()
            print(f"✅ Connected to {self.port}")
            return True
        except serial.SerialException as e:
            print(f"❌ Connection failed: {e}")
            return False

    def disconnect(self):
        """Clean disconnect."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print(f"🔌 Disconnected from {self.port}")

    def send_and_read(self, cmd, timeout=5.0):
        """Send a command and read response lines."""
        if not self.ser:
            return []

        self.ser.reset_input_buffer()
        self.ser.write(f"{cmd}\r\n".encode())
        self.ser.flush()

        lines = []
        start = time.time()
        while (time.time() - start) < timeout:
            if self.ser.in_waiting:
                line = self.ser.readline().decode("utf-8", errors="replace").strip()
                if line:
                    lines.append(line)
                start = time.time()
            else:
                time.sleep(0.05)
        return lines

    def detect_firmware(self):
        """Detect whether WiFi devboard runs Marauder, AT firmware, or other."""
        # Try Marauder first
        print("🔍 Detecting WiFi devboard firmware...")

        # Enter WiFi devboard mode on Flipper (Ctrl+Q for GPIO passthrough)
        # For direct devboard connection, we query directly
        response = self.send_and_read("version", timeout=3.0)
        version_text = "\n".join(response).lower()

        if "marauder" in version_text:
            self.firmware_type = "marauder"
            print(f"   Detected: ESP32 Marauder")
            return "marauder"

        # Try AT firmware
        response = self.send_and_read("AT", timeout=2.0)
        if any("OK" in line for line in response):
            self.firmware_type = "at"
            print(f"   Detected: Stock AT Firmware")
            return "at"

        # Try Flipper CLI wifi scan
        response = self.send_and_read("wifi scan", timeout=2.0)
        if response:
            self.firmware_type = "flipper_cli"
            print(f"   Detected: Flipper CLI WiFi mode")
            return "flipper_cli"

        # Try Blackmagic
        response = self.send_and_read("help", timeout=2.0)
        if any("blackmagic" in line.lower() for line in response):
            self.firmware_type = "blackmagic"
            print(f"   Detected: Blackmagic Debug Probe")
            return "blackmagic"

        self.firmware_type = "unknown"
        print("   ⚠️  Firmware type could not be determined")
        return "unknown"

    def scan_aps_marauder(self, duration=10):
        """Run AP scan using Marauder firmware."""
        print(f"📡 Starting Marauder AP scan ({duration}s)...")
        self.send_and_read("scanap", timeout=1.0)
        time.sleep(duration)
        self.send_and_read("stopscan", timeout=2.0)
        time.sleep(1.0)

        # Retrieve results
        lines = self.send_and_read("list -a", timeout=5.0)
        return self._parse_marauder_aps(lines)

    def scan_aps_at(self, duration=10):
        """Run AP scan using AT firmware."""
        print(f"📡 Starting AT firmware AP scan...")
        lines = self.send_and_read("AT+CWLAP", timeout=duration + 5)
        return self._parse_at_aps(lines)

    def scan_aps_flipper_cli(self, duration=10):
        """Run AP scan using Flipper CLI wifi module."""
        print(f"📡 Starting Flipper CLI WiFi scan...")
        lines = self.send_and_read("wifi scan", timeout=duration + 5)
        return self._parse_flipper_aps(lines)

    def scan(self, duration=10):
        """Run AP scan using detected firmware."""
        if not self.firmware_type:
            self.detect_firmware()

        scan_method = {
            "marauder": self.scan_aps_marauder,
            "at": self.scan_aps_at,
            "flipper_cli": self.scan_aps_flipper_cli,
        }.get(self.firmware_type)

        if not scan_method:
            print(f"❌ Scanning not supported for firmware: {self.firmware_type}")
            return []

        start_time = time.time()
        results = scan_method(duration)
        elapsed = round(time.time() - start_time, 1)

        print(f"\n📊 Scan complete: {len(results)} APs found in {elapsed}s")
        return results

    @staticmethod
    def _parse_marauder_aps(lines):
        """Parse Marauder `list -a` output into structured data."""
        aps = []
        for line in lines:
            # Marauder format: [index] SSID (CH: X, RSSI: Y) BSSID
            match = re.match(
                r"\[?\d+\]?\s+(.+?)\s+\(CH:\s*(\d+),\s*RSSI:\s*(-?\d+)\)\s+([0-9A-Fa-f:]{17})",
                line,
            )
            if match:
                aps.append({
                    "ssid": match.group(1).strip(),
                    "channel": int(match.group(2)),
                    "rssi": int(match.group(3)),
                    "bssid": match.group(4).upper(),
                })
        return aps

    @staticmethod
    def _parse_at_aps(lines):
        """Parse AT+CWLAP output."""
        aps = []
        for line in lines:
            # AT format: +CWLAP:(security,ssid,rssi,mac,channel)
            match = re.match(
                r"\+CWLAP:\((\d+),\"(.+?)\",(-?\d+),\"([0-9A-Fa-f:]{17})\",(\d+)",
                line,
            )
            if match:
                aps.append({
                    "security": int(match.group(1)),
                    "ssid": match.group(2),
                    "rssi": int(match.group(3)),
                    "bssid": match.group(4).upper(),
                    "channel": int(match.group(5)),
                })
        return aps

    @staticmethod
    def _parse_flipper_aps(lines):
        """Parse Flipper CLI wifi scan output."""
        aps = []
        for line in lines:
            # Generic: look for SSID, channel, signal patterns
            parts = line.split(",")
            if len(parts) >= 3:
                try:
                    aps.append({
                        "ssid": parts[0].strip(),
                        "channel": int(parts[1].strip()) if parts[1].strip().isdigit() else 0,
                        "rssi": int(parts[2].strip()) if parts[2].strip().lstrip("-").isdigit() else 0,
                    })
                except (ValueError, IndexError):
                    pass
        return aps


def save_results(results, output_dir, fmt="json"):
    """Save scan results to file."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = generate_filename(output_dir, fmt)

    scan_metadata = {
        "scan_time": datetime.now(timezone.utc).isoformat(),
        "total_aps": len(results),
        "access_points": results,
    }

    if fmt == "json":
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(scan_metadata, f, indent=2)
    elif fmt == "csv":
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            if results:
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
            else:
                f.write("# No results\n")

    print(f"💾 Results saved: {filepath}")
    return filepath


def main():
    parser = argparse.ArgumentParser(
        description="Flipper Zero WiFi Scan Launcher — trigger scans, parse & save results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--port", type=str, help="COM port (auto-detect if omitted)")
    parser.add_argument("--duration", type=int, default=10, help="Scan duration in seconds (default: 10)")
    parser.add_argument("--output", type=str, default=DEFAULT_CAPTURES_DIR, help="Output directory")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Output format")
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

    # Connect and scan
    scanner = WiFiScanner(port, args.baud)
    if not scanner.connect():
        sys.exit(1)

    try:
        results = scanner.scan(duration=args.duration)
        if results:
            filepath = save_results(results, args.output, args.format)
            print(f"\n📋 Summary:")
            print(f"   APs found:     {len(results)}")
            print(f"   Output format:  {args.format}")
            print(f"   Saved to:       {filepath}")
        else:
            print("\n⚠️  No access points found. Check WiFi devboard connection.")
    finally:
        scanner.disconnect()


if __name__ == "__main__":
    main()
