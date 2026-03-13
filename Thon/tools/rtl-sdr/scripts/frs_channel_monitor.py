#!/usr/bin/env python3
"""FRS/GMRS Channel Monitor — Configurable radio signal detector.

Usage:
    python frs_channel_monitor.py --channel 1 --sub 1
    python frs_channel_monitor.py -c 7 -s 10
    python frs_channel_monitor.py -c 1                    # No CTCSS filter
    python frs_channel_monitor.py -c 1 -s 1 --gain 30    # Custom gain
    python frs_channel_monitor.py --list-channels         # Show all channels
    python frs_channel_monitor.py --list-subs             # Show all sub-channels
"""

import argparse
import time
import sys
import os
import numpy as np

# ---------------------------------------------------------------------------
# DLL resolution — find librtlsdr.dll in parent tools directory
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.dirname(SCRIPT_DIR)
os.add_dll_directory(TOOLS_DIR)

from rtlsdr import RtlSdr

# ---------------------------------------------------------------------------
# FRS/GMRS Channel Table (22 standard channels)
# ---------------------------------------------------------------------------
FRS_CHANNELS = {
    1:  462.5625e6,
    2:  462.5875e6,
    3:  462.6125e6,
    4:  462.6375e6,
    5:  462.6625e6,
    6:  462.6875e6,
    7:  462.7125e6,
    8:  467.5625e6,
    9:  467.5875e6,
    10: 467.6125e6,
    11: 467.6375e6,
    12: 467.6625e6,
    13: 467.6875e6,
    14: 467.7125e6,
    15: 462.5500e6,
    16: 462.5750e6,
    17: 462.6000e6,
    18: 462.6250e6,
    19: 462.6500e6,
    20: 462.6750e6,
    21: 462.7000e6,
    22: 462.7250e6,
}

# ---------------------------------------------------------------------------
# CTCSS Sub-Channel Tone Table (38 standard tones)
# Sub-channel 0 = no tone (open squelch)
# ---------------------------------------------------------------------------
CTCSS_TONES = {
    0:  None,      # No tone / open squelch
    1:  67.0,
    2:  71.9,
    3:  74.4,
    4:  77.0,
    5:  79.7,
    6:  82.5,
    7:  85.4,
    8:  88.5,
    9:  91.5,
    10: 94.8,
    11: 97.4,
    12: 100.0,
    13: 103.5,
    14: 107.2,
    15: 110.9,
    16: 114.8,
    17: 118.8,
    18: 123.0,
    19: 127.3,
    20: 131.8,
    21: 136.5,
    22: 141.3,
    23: 146.2,
    24: 151.4,
    25: 156.7,
    26: 162.2,
    27: 167.9,
    28: 173.8,
    29: 179.9,
    30: 186.2,
    31: 192.8,
    32: 203.5,
    33: 210.7,
    34: 218.1,
    35: 225.7,
    36: 233.6,
    37: 241.8,
    38: 250.3,
}

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
DEFAULT_SAMPLE_RATE = 2.048e6
DEFAULT_GAIN = 40           # dB
DEFAULT_NUM_SAMPLES = 256 * 1024  # ~125ms per capture
NOISE_FLOOR_SAMPLES = 5
DETECTION_THRESHOLD_DB = 6  # dB above noise floor


# ===========================================================================
# Signal processing
# ===========================================================================

def compute_power_db(samples: np.ndarray) -> float:
    """Average power in dB from complex IQ samples."""
    power = np.mean(np.abs(samples) ** 2)
    return 10 * np.log10(power) if power > 0 else -999.0


def detect_ctcss(samples: np.ndarray, sample_rate: float,
                 target_tone: float, tolerance: float = 2.0):
    """Detect a CTCSS sub-audible tone via FM demodulation + FFT.

    Returns (detected: bool, snr: float).
    """
    phase = np.angle(samples)
    freq_inst = np.diff(np.unwrap(phase)) * sample_rate / (2 * np.pi)

    window = int(sample_rate / 1000)
    if window > 0 and len(freq_inst) > window:
        audio = np.convolve(freq_inst, np.ones(window) / window, mode='valid')
        fft = np.abs(np.fft.rfft(audio))
        freqs = np.fft.rfftfreq(len(audio), d=1.0 / sample_rate)

        mask = (freqs >= target_tone - tolerance) & (freqs <= target_tone + tolerance)
        if np.any(mask):
            tone_power = np.max(fft[mask])
            avg_power = np.mean(fft)
            if avg_power > 0:
                snr = tone_power / avg_power
                return snr > 3.0, snr
    return False, 0.0


# ===========================================================================
# Display helpers
# ===========================================================================

def print_channel_table():
    """Print all FRS/GMRS channels."""
    print("FRS/GMRS Channel Table")
    print("-" * 40)
    print(f"{'Ch':>4}  {'Frequency':>14}  {'Band'}")
    print("-" * 40)
    for ch, freq in sorted(FRS_CHANNELS.items()):
        band = "FRS/GMRS" if freq < 467e6 else "FRS only"
        print(f"  {ch:>2}   {freq / 1e6:>10.4f} MHz   {band}")


def print_sub_table():
    """Print all CTCSS tones."""
    print("CTCSS Sub-Channel Tone Table")
    print("-" * 30)
    print(f"{'Sub':>4}  {'Tone (Hz)':>10}")
    print("-" * 30)
    for sub, tone in sorted(CTCSS_TONES.items()):
        if tone is None:
            print(f"  {sub:>2}   {'none':>10}  (open squelch)")
        else:
            print(f"  {sub:>2}   {tone:>10.1f}")


# ===========================================================================
# Main monitor
# ===========================================================================

def monitor(channel: int, sub: int, gain: float,
            sample_rate: float, num_samples: int):
    """Run the FRS channel monitor loop."""

    freq = FRS_CHANNELS[channel]
    ctcss_tone = CTCSS_TONES.get(sub)

    print("=" * 60)
    print(f"FRS CHANNEL {channel} MONITOR")
    print("=" * 60)
    print(f"  Channel:      {channel}")
    print(f"  Frequency:    {freq / 1e6:.4f} MHz")
    if ctcss_tone:
        print(f"  Sub-channel:  {sub} (CTCSS {ctcss_tone:.1f} Hz)")
    else:
        print(f"  Sub-channel:  {sub} (no tone / open)")
    print(f"  Sample Rate:  {sample_rate / 1e6:.3f} MHz")
    print(f"  Gain:         {gain} dB")
    print(f"  Samples/Read: {num_samples}")
    print()

    # --- Open SDR ---
    try:
        sdr = RtlSdr()
    except Exception as e:
        print(f"[!] Failed to open SDR: {e}")
        sys.exit(1)

    sdr.sample_rate = sample_rate
    sdr.center_freq = freq
    sdr.gain = gain

    print(f"  Tuner type:   {sdr.get_tuner_type()}")
    print(f"  Actual freq:  {sdr.center_freq / 1e6:.4f} MHz")
    print()

    # --- Establish noise floor ---
    print("[*] Establishing noise floor (DO NOT TRANSMIT)...")
    noise_readings = []
    for i in range(NOISE_FLOOR_SAMPLES):
        samples = sdr.read_samples(num_samples)
        pwr = compute_power_db(samples)
        noise_readings.append(pwr)
        print(f"    Baseline {i + 1}/{NOISE_FLOOR_SAMPLES}: {pwr:.2f} dB")

    noise_floor = np.mean(noise_readings)
    threshold = noise_floor + DETECTION_THRESHOLD_DB

    print(f"\n[*] Noise floor: {noise_floor:.2f} dB")
    print(f"[*] Detection threshold: {threshold:.2f} dB "
          f"(+{DETECTION_THRESHOLD_DB} dB)")
    print()
    print("=" * 60)
    print("LISTENING — Key your radio now!")
    print("Press Ctrl+C to stop")
    print("=" * 60)

    # --- Monitor loop ---
    try:
        capture_num = 0
        while True:
            samples = sdr.read_samples(num_samples)
            power_db = compute_power_db(samples)
            capture_num += 1
            timestamp = time.strftime("%H:%M:%S")
            delta = power_db - noise_floor

            if power_db > threshold:
                # Signal detected — check CTCSS if configured
                ctcss_str = ""
                if ctcss_tone:
                    found, snr = detect_ctcss(samples, sample_rate, ctcss_tone)
                    label = "YES" if found else "no"
                    ctcss_str = f" | CTCSS {ctcss_tone:.1f}Hz: {label} (SNR {snr:.1f})"

                print(f"  [{timestamp}] >>>  SIGNAL  "
                      f"{power_db:+.2f} dB  (Δ {delta:+.2f} dB){ctcss_str}")
            else:
                if capture_num % 10 == 0:
                    print(f"  [{timestamp}]      quiet   "
                          f"{power_db:+.2f} dB  (Δ {delta:+.2f} dB)")

    except KeyboardInterrupt:
        print("\n[*] Stopped by user.")
    finally:
        sdr.close()
        print("[*] SDR closed.")


# ===========================================================================
# CLI
# ===========================================================================

def main():
    parser = argparse.ArgumentParser(
        description="FRS/GMRS Channel Monitor — RTL-SDR signal detector",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s -c 1 -s 1          Monitor Ch 1, Sub-ch 1\n"
            "  %(prog)s -c 7               Monitor Ch 7, no CTCSS\n"
            "  %(prog)s -c 1 --gain 30     Custom gain\n"
            "  %(prog)s --list-channels     Show channel table\n"
            "  %(prog)s --list-subs         Show CTCSS tone table\n"
        ),
    )
    parser.add_argument("-c", "--channel", type=int,
                        help="FRS/GMRS channel number (1-22)")
    parser.add_argument("-s", "--sub", type=int, default=0,
                        help="Sub-channel / CTCSS code (0-38, default: 0 = none)")
    parser.add_argument("--gain", type=float, default=DEFAULT_GAIN,
                        help=f"Tuner gain in dB (default: {DEFAULT_GAIN})")
    parser.add_argument("--list-channels", action="store_true",
                        help="Print the FRS/GMRS channel frequency table")
    parser.add_argument("--list-subs", action="store_true",
                        help="Print the CTCSS sub-channel tone table")

    args = parser.parse_args()

    if args.list_channels:
        print_channel_table()
        return
    if args.list_subs:
        print_sub_table()
        return

    if args.channel is None:
        parser.error("--channel / -c is required (or use --list-channels)")

    if args.channel not in FRS_CHANNELS:
        parser.error(f"Invalid channel {args.channel}. Valid: 1-22")
    if args.sub not in CTCSS_TONES:
        parser.error(f"Invalid sub-channel {args.sub}. Valid: 0-38")

    monitor(
        channel=args.channel,
        sub=args.sub,
        gain=args.gain,
        sample_rate=DEFAULT_SAMPLE_RATE,
        num_samples=DEFAULT_NUM_SAMPLES,
    )


if __name__ == "__main__":
    main()
