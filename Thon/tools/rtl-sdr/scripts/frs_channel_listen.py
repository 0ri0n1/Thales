#!/usr/bin/env python3
"""FRS/GMRS Channel Listener — Real-time FM demod with speaker output.

Tunes the RTL-SDR to an FRS/GMRS channel, demodulates narrowband FM,
applies de-emphasis filtering, and plays audio through speakers.

Usage:
    python frs_channel_listen.py -c 1 -s 1
    python frs_channel_listen.py -c 7 --gain 30
    python frs_channel_listen.py -c 1 --volume 3
"""

import argparse
import sys
import os
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.dirname(SCRIPT_DIR)
os.add_dll_directory(TOOLS_DIR)

import sounddevice as sd
from rtlsdr import RtlSdr

# ---------------------------------------------------------------------------
# FRS/GMRS Channel Table
# ---------------------------------------------------------------------------
FRS_CHANNELS = {
    1:  462.5625e6,  2:  462.5875e6,  3:  462.6125e6,  4:  462.6375e6,
    5:  462.6625e6,  6:  462.6875e6,  7:  462.7125e6,  8:  467.5625e6,
    9:  467.5875e6,  10: 467.6125e6,  11: 467.6375e6,  12: 467.6625e6,
    13: 467.6875e6,  14: 467.7125e6,  15: 462.5500e6,  16: 462.5750e6,
    17: 462.6000e6,  18: 462.6250e6,  19: 462.6500e6,  20: 462.6750e6,
    21: 462.7000e6,  22: 462.7250e6,
}

CTCSS_TONES = {
    0: None, 1: 67.0, 2: 71.9, 3: 74.4, 4: 77.0, 5: 79.7, 6: 82.5,
    7: 85.4, 8: 88.5, 9: 91.5, 10: 94.8, 11: 97.4, 12: 100.0,
    13: 103.5, 14: 107.2, 15: 110.9, 16: 114.8, 17: 118.8, 18: 123.0,
    19: 127.3, 20: 131.8, 21: 136.5, 22: 141.3, 23: 146.2, 24: 151.4,
    25: 156.7, 26: 162.2, 27: 167.9, 28: 173.8, 29: 179.9, 30: 186.2,
    31: 192.8, 32: 203.5, 33: 210.7, 34: 218.1, 35: 225.7, 36: 233.6,
    37: 241.8, 38: 250.3,
}

# ---------------------------------------------------------------------------
# SDR + Audio config
# ---------------------------------------------------------------------------
SDR_SAMPLE_RATE = 240000     # 240 kHz — good for NBFM
AUDIO_RATE = 48000           # Standard audio output rate
DECIMATION = SDR_SAMPLE_RATE // AUDIO_RATE  # 5x decimation
CHUNK_SAMPLES = 128 * 1024   # Smaller chunks for lower latency
DEFAULT_GAIN = 49.6          # Max gain for the R820T2
DEFAULT_VOLUME = 3.0         # Boosted default volume


# ===========================================================================
# Signal processing
# ===========================================================================

def fm_demodulate(iq_samples):
    """FM demodulate using polar discriminator."""
    return np.angle(iq_samples[1:] * np.conj(iq_samples[:-1]))


def de_emphasis_filter(audio, sample_rate, tau=750e-6):
    """Apply de-emphasis filter to remove FM pre-emphasis hiss.

    Args:
        audio: Demodulated audio samples.
        sample_rate: Audio sample rate.
        tau: De-emphasis time constant (750μs for NBFM in North America).
    Returns:
        Filtered audio with reduced high-frequency noise.
    """
    # Single-pole IIR low-pass: y[n] = alpha * x[n] + (1-alpha) * y[n-1]
    alpha = 1.0 / (1.0 + sample_rate * tau)
    filtered = np.zeros_like(audio)
    filtered[0] = alpha * audio[0]
    for i in range(1, len(audio)):
        filtered[i] = alpha * audio[i] + (1.0 - alpha) * filtered[i - 1]
    return filtered


def de_emphasis_filter_fast(audio, sample_rate, tau=750e-6):
    """Vectorized de-emphasis using scipy if available, else pure numpy."""
    alpha = 1.0 / (1.0 + sample_rate * tau)
    try:
        from scipy.signal import lfilter
        return lfilter([alpha], [1.0, -(1.0 - alpha)], audio).astype(np.float64)
    except ImportError:
        # Fallback to loop
        return de_emphasis_filter(audio, sample_rate, tau)


def low_pass_decimate(signal, decimation):
    """Low-pass filter + decimate by averaging groups."""
    n = len(signal) - (len(signal) % decimation)
    signal = signal[:n]
    return signal.reshape(-1, decimation).mean(axis=1)


def bandpass_voice(audio, sample_rate):
    """Simple voice bandpass: keep 300-3400 Hz for speech clarity."""
    try:
        from scipy.signal import butter, lfilter
        nyq = sample_rate / 2.0
        low = 300.0 / nyq
        high = 3400.0 / nyq
        b, a = butter(4, [low, high], btype='band')
        return lfilter(b, a, audio)
    except ImportError:
        return audio  # Skip if no scipy


def compute_power_db(samples):
    """Average power in dB."""
    power = np.mean(np.abs(samples) ** 2)
    return 10 * np.log10(power) if power > 0 else -999.0


# ===========================================================================
# Main
# ===========================================================================

def main():
    parser = argparse.ArgumentParser(
        description="FRS/GMRS Channel Listener — live audio through speakers")
    parser.add_argument("-c", "--channel", type=int, required=True,
                        help="FRS/GMRS channel (1-22)")
    parser.add_argument("-s", "--sub", type=int, default=0,
                        help="Sub-channel / CTCSS code (0-38, default: 0)")
    parser.add_argument("--gain", type=float, default=DEFAULT_GAIN,
                        help=f"Tuner gain in dB (default: {DEFAULT_GAIN})")
    parser.add_argument("--volume", type=float, default=DEFAULT_VOLUME,
                        help=f"Audio volume multiplier (default: {DEFAULT_VOLUME})")
    parser.add_argument("--squelch", type=float, default=6.0,
                        help="Squelch threshold dB above noise (default: 6)")
    parser.add_argument("--raw", action="store_true",
                        help="Disable de-emphasis and voice filters")
    args = parser.parse_args()

    if args.channel not in FRS_CHANNELS:
        parser.error("Invalid channel. Valid: 1-22")

    freq = FRS_CHANNELS[args.channel]
    ctcss = CTCSS_TONES.get(args.sub)

    print("=" * 60)
    print(f"FRS CHANNEL {args.channel} LISTENER")
    print("=" * 60)
    print(f"  Frequency:    {freq / 1e6:.4f} MHz")
    if ctcss:
        print(f"  Sub-channel:  {args.sub} (CTCSS {ctcss:.1f} Hz)")
    else:
        print(f"  Sub-channel:  none (open squelch)")
    print(f"  SDR rate:     {SDR_SAMPLE_RATE / 1e3:.0f} kHz")
    print(f"  Audio rate:   {AUDIO_RATE} Hz")
    print(f"  Gain:         {args.gain} dB")
    print(f"  Volume:       {args.volume}x")
    print(f"  Squelch:      +{args.squelch} dB above noise")
    print(f"  Filters:      {'off (raw)' if args.raw else 'de-emphasis + voice bandpass'}")
    print()

    dev = sd.query_devices(kind='output')
    print(f"  Audio output: {dev['name']}")
    print()

    try:
        sdr = RtlSdr()
    except Exception as e:
        print(f"[!] Failed to open SDR: {e}")
        sys.exit(1)

    sdr.sample_rate = SDR_SAMPLE_RATE
    sdr.center_freq = freq
    sdr.gain = args.gain

    print(f"  Tuner:        {sdr.get_tuner_type()}")
    print(f"  Actual freq:  {sdr.center_freq / 1e6:.4f} MHz")
    print()

    # Noise floor
    print("[*] Establishing noise floor...")
    noise_readings = []
    for i in range(5):
        samples = sdr.read_samples(CHUNK_SAMPLES)
        noise_readings.append(compute_power_db(samples))
    noise_floor = np.mean(noise_readings)
    threshold = noise_floor + args.squelch
    print(f"    Noise floor: {noise_floor:.1f} dB")
    print(f"    Squelch at:  {threshold:.1f} dB")
    print()
    print("=" * 60)
    print("LISTENING — audio plays when signal detected")
    print("Press Ctrl+C to stop")
    print("=" * 60)

    stream = sd.OutputStream(
        samplerate=AUDIO_RATE,
        channels=1,
        dtype='float32',
        blocksize=4096,
    )
    stream.start()

    try:
        chunk_count = 0
        while True:
            iq = sdr.read_samples(CHUNK_SAMPLES)
            power = compute_power_db(iq)
            chunk_count += 1

            if power > threshold:
                # --- Demodulate ---
                audio = fm_demodulate(iq)

                # --- Decimate to audio rate ---
                audio = low_pass_decimate(audio, DECIMATION)

                # --- De-emphasis: remove FM hiss ---
                if not args.raw:
                    audio = de_emphasis_filter_fast(audio, AUDIO_RATE)
                    audio = bandpass_voice(audio, AUDIO_RATE)

                # --- Normalize + volume ---
                peak = np.max(np.abs(audio))
                if peak > 0:
                    audio = audio / peak
                audio = np.clip(audio * args.volume, -1.0, 1.0)
                audio = audio.astype(np.float32)

                stream.write(audio)

                delta = power - noise_floor
                if chunk_count % 3 == 0:
                    print(f"  [AUDIO] {power:+.1f} dB "
                          f"(+{delta:.0f} dB) | {len(audio)} samples")
            else:
                silence = np.zeros(1024, dtype=np.float32)
                stream.write(silence)
                if chunk_count % 20 == 0:
                    print(f"  [quiet] {power:+.1f} dB")

    except KeyboardInterrupt:
        print("\n[*] Stopped.")
    finally:
        stream.stop()
        stream.close()
        sdr.close()
        print("[*] Audio and SDR closed.")


if __name__ == "__main__":
    main()
