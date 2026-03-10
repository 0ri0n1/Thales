#!/usr/bin/env python3
"""
Analyze monitor-mode pcap for Tuya EZ Mode pairing broadcasts.

Tuya EZ mode encodes data into UDP broadcast packet lengths.
The preamble is a sequence of packets with relative lengths: 1, 3, 6, 10
(offset from a base of ~49 bytes).

We look for:
1. Broadcast frames from a single source MAC
2. Rapidly repeating length patterns (the preamble)
3. Decode the subsequent data lengths into bytes
"""
import struct
import json
import sys
from collections import defaultdict

PCAP_FILE = sys.argv[1] if len(sys.argv) > 1 else "/tmp/tuya_pairing3.pcap"

def read_pcap(filename):
    """Read pcap file and yield (timestamp, raw_frame) tuples."""
    with open(filename, 'rb') as f:
        magic = struct.unpack('<I', f.read(4))[0]
        if magic == 0xa1b2c3d4:
            endian = '<'
        elif magic == 0xd4c3b2a1:
            endian = '>'
        else:
            print(f"Unknown pcap magic: {hex(magic)}")
            return

        version_major, version_minor, tz_offset, tz_accuracy, snap_len, link_type = \
            struct.unpack(endian + 'HHIIII', f.read(20))
        
        print(f"PCAP: link_type={link_type}, snap_len={snap_len}")
        
        while True:
            hdr = f.read(16)
            if len(hdr) < 16:
                break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(endian + 'IIII', hdr)
            data = f.read(incl_len)
            if len(data) < incl_len:
                break
            yield (ts_sec + ts_usec / 1e6, data, orig_len)


def parse_80211_frame(data):
    """Parse 802.11 frame header. Returns (type, subtype, addr1, addr2, frame_len) or None."""
    if len(data) < 24:
        return None
    
    # Check for radiotap header
    if data[0] == 0x00 and data[1] == 0x00:
        rt_len = struct.unpack('<H', data[2:4])[0]
        data = data[rt_len:]
        if len(data) < 24:
            return None
    
    fc = struct.unpack('<H', data[0:2])[0]
    frame_type = (fc >> 2) & 0x3
    frame_subtype = (fc >> 4) & 0xf
    
    addr1 = data[4:10]
    addr2 = data[10:16]
    
    return (frame_type, frame_subtype, addr1, addr2, len(data))


def mac_str(raw):
    return ':'.join(f'{b:02x}' for b in raw)


def is_broadcast(addr):
    return addr == b'\xff\xff\xff\xff\xff\xff'


def find_ez_mode_patterns(frames):
    """Find sources that send many broadcast frames with varying lengths — EZ mode signature."""
    
    src_broadcasts = defaultdict(list)
    
    for ts, frame_type, subtype, addr1, addr2, frame_len in frames:
        if frame_type == 2 and is_broadcast(addr1):
            src = mac_str(addr2)
            src_broadcasts[src].append((ts, frame_len))
    
    print(f"\n=== Broadcast sources (data frames) ===")
    for src, pkts in sorted(src_broadcasts.items(), key=lambda x: -len(x[1])):
        if len(pkts) < 20:
            continue
        lengths = [p[1] for p in pkts]
        unique_lens = len(set(lengths))
        duration = pkts[-1][0] - pkts[0][0] if len(pkts) > 1 else 0
        print(f"  {src}: {len(pkts)} frames, {unique_lens} unique lengths, {duration:.1f}s span")
        
        if unique_lens > 5 and len(pkts) > 30:
            print(f"    -> CANDIDATE for EZ mode (high length variation)")
            print(f"    First 50 lengths: {lengths[:50]}")
    
    return src_broadcasts


def decode_tuya_ez(lengths, base_offset=49):
    """Try to decode Tuya EZ mode from packet lengths."""
    data = bytearray()
    for l in lengths:
        v = l - base_offset
        if 0 <= v <= 255:
            data.append(v)
    return data


def try_all_offsets(lengths):
    """Try different base offsets to find one that produces readable data."""
    results = []
    for offset in range(30, 120):
        decoded = decode_tuya_ez(lengths, offset)
        printable = sum(1 for b in decoded if 32 <= b <= 126)
        ratio = printable / len(decoded) if decoded else 0
        if ratio > 0.3 and len(decoded) > 10:
            results.append((offset, ratio, decoded))
    
    results.sort(key=lambda x: -x[1])
    return results[:5]


print(f"Reading {PCAP_FILE}...")

frames = []
total = 0
for ts, data, orig_len in read_pcap(PCAP_FILE):
    total += 1
    parsed = parse_80211_frame(data)
    if parsed:
        frame_type, subtype, addr1, addr2, flen = parsed
        frames.append((ts, frame_type, subtype, addr1, addr2, orig_len))

print(f"Total packets: {total}")
print(f"Parsed 802.11 frames: {len(frames)}")

# Count frame types
type_counts = defaultdict(int)
for ts, ft, st, a1, a2, fl in frames:
    type_counts[(ft, st)] += 1
print(f"\nFrame types: { {f'type{k[0]}/sub{k[1]}': v for k,v in sorted(type_counts.items())} }")

# Find EZ mode candidates
src_broadcasts = find_ez_mode_patterns(frames)

# Try to decode from top candidates
print(f"\n=== Attempting EZ mode decode ===")
for src, pkts in sorted(src_broadcasts.items(), key=lambda x: -len(x[1])):
    if len(pkts) < 30:
        continue
    
    lengths = [p[1] for p in pkts]
    unique = len(set(lengths))
    
    if unique < 5:
        continue
    
    print(f"\nSource: {src} ({len(pkts)} packets, {unique} unique lengths)")
    
    best = try_all_offsets(lengths)
    if best:
        for offset, ratio, decoded in best:
            print(f"  Offset {offset}: {ratio:.1%} printable")
            print(f"    Hex: {decoded[:64].hex()}")
            try:
                text = decoded[:64].decode('utf-8', errors='replace')
                print(f"    Text: {text}")
            except:
                pass
    
    # Also try finding preamble pattern within the lengths
    for i in range(len(lengths) - 3):
        diffs = [lengths[i+j+1] - lengths[i+j] for j in range(3)]
        if diffs == [2, 3, 4]:
            print(f"  PREAMBLE found at index {i}! lengths[{i}:{i+4}] = {lengths[i:i+4]}")
            post_preamble = lengths[i+4:]
            decoded = decode_tuya_ez(post_preamble)
            print(f"  Post-preamble decoded ({len(decoded)} bytes): {decoded[:80].hex()}")
            try:
                print(f"  As text: {decoded[:80].decode('utf-8', errors='replace')}")
            except:
                pass
            break

print("\nDONE")
