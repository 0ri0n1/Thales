#!/usr/bin/env python3
"""
Ready-to-run extraction script.
Run with: python3 ready_to_extract.py <ACCESS_ID> <ACCESS_SECRET>

Uses tinytuya Cloud API with Tuya IoT Platform credentials.
Will try all regions automatically.
"""
import sys
import json
import tinytuya

if len(sys.argv) < 3:
    print("Usage: python3 ready_to_extract.py <ACCESS_ID> <ACCESS_SECRET>")
    print()
    print("Get these from https://iot.tuya.com -> Cloud -> Development -> Your Project")
    sys.exit(1)

ACCESS_ID = sys.argv[1]
ACCESS_SECRET = sys.argv[2]

print(f"Access ID: {ACCESS_ID}")
print(f"Access Secret: {ACCESS_SECRET[:8]}...")
print()

for region in ["us", "eu", "cn", "in"]:
    print(f"Trying region: {region}...")
    try:
        c = tinytuya.Cloud(
            apiRegion=region,
            apiKey=ACCESS_ID,
            apiSecret=ACCESS_SECRET,
        )
        devices = c.getdevices()
        if devices and isinstance(devices, list) and len(devices) > 0:
            print(f"\nSUCCESS! Found {len(devices)} device(s) in region '{region}':\n")
            for d in devices:
                print(f"  Name:      {d.get('name', 'N/A')}")
                print(f"  Device ID: {d.get('id', 'N/A')}")
                print(f"  LOCAL KEY: {d.get('key', 'N/A')}")
                print(f"  MAC:       {d.get('mac', 'N/A')}")
                print(f"  Category:  {d.get('category', 'N/A')}")
                print(f"  Product:   {d.get('product_id', 'N/A')}")
                print(f"  UUID:      {d.get('uuid', 'N/A')}")
                print()

            with open('/tmp/tuya_devices_final.json', 'w') as f:
                json.dump(devices, f, indent=2)
            print("Full data saved to /tmp/tuya_devices_final.json")
            sys.exit(0)
        else:
            err = getattr(c, 'error', 'unknown')
            print(f"  No devices found. Error: {err}")
    except Exception as e:
        print(f"  Error: {type(e).__name__}: {e}")

print("\nNo devices found in any region.")
print("Make sure you've linked your Lampux/Tuya app account to the IoT project.")
