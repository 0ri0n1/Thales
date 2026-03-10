#!/usr/bin/env python3
"""
Tuya IoT Platform key extraction.
Requires: ACCESS_ID and ACCESS_SECRET from iot.tuya.com
"""
import sys
import json
import tinytuya

ACCESS_ID = sys.argv[1] if len(sys.argv) > 1 else ""
ACCESS_SECRET = sys.argv[2] if len(sys.argv) > 2 else ""

if not ACCESS_ID or not ACCESS_SECRET:
    print("Usage: python3 extract_key_iot.py <ACCESS_ID> <ACCESS_SECRET>")
    sys.exit(1)

print(f"Connecting to Tuya IoT Platform...")
print(f"ACCESS_ID: {ACCESS_ID[:8]}...")
print(f"ACCESS_SECRET: {ACCESS_SECRET[:8]}...")

c = tinytuya.Cloud(
    apiRegion="us",
    apiKey=ACCESS_ID,
    apiSecret=ACCESS_SECRET,
)

print("\nFetching device list...")
devices = c.getdevices()

if not devices:
    print("No devices found. Trying EU region...")
    c = tinytuya.Cloud(
        apiRegion="eu",
        apiKey=ACCESS_ID,
        apiSecret=ACCESS_SECRET,
    )
    devices = c.getdevices()

if not devices:
    print("Still no devices. Check that you've linked your Lampux account to the IoT project.")
    sys.exit(1)

print(f"\nFound {len(devices)} device(s):\n")

for dev in devices:
    print(f"  Name: {dev.get('name', 'Unknown')}")
    print(f"  ID: {dev.get('id', 'Unknown')}")
    print(f"  LOCAL KEY: {dev.get('key', 'NOT FOUND')}")
    print(f"  MAC: {dev.get('mac', 'Unknown')}")
    print(f"  Category: {dev.get('category', 'Unknown')}")
    print(f"  Product ID: {dev.get('product_id', 'Unknown')}")
    print(f"  UUID: {dev.get('uuid', 'Unknown')}")
    print(f"  IP: {dev.get('ip', 'Unknown')}")
    print()

with open('/tmp/tuya_devices.json', 'w') as f:
    json.dump(devices, f, indent=2)
print("Saved full device data to /tmp/tuya_devices.json")
