#!/usr/bin/env python3
"""RTL-SDR Device Validation Script

Tests device connectivity, reports hardware info, and captures
a quick sample to validate the full signal chain.
"""

import subprocess
import sys
import os

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))


def run_cli_tool(tool_name, args=None, timeout=10):
    """Run an rtl-sdr CLI tool and return output."""
    exe = os.path.join(TOOLS_DIR, f"{tool_name}.exe")
    if not os.path.exists(exe):
        print(f"  [!] {tool_name}.exe not found at {exe}")
        return None
    cmd = [exe] + (args or [])
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return f"[!] {tool_name} timed out after {timeout}s"
    except Exception as e:
        return f"[!] {tool_name} error: {e}"


def test_device_detection():
    """Phase 1: Check if rtl_test can find the device."""
    print("=" * 60)
    print("PHASE 1: Device Detection (rtl_test)")
    print("=" * 60)
    output = run_cli_tool("rtl_test", ["-t"], timeout=5)
    if output is None:
        return False
    print(output)
    found = "Found 1 device" in output or "R820T" in output
    if found:
        print("  [OK] Device detected!")
    else:
        print("  [FAIL] No RTL-SDR device found.")
        print("  Check: Is the WinUSB driver installed via Zadig?")
    return found


def test_python_sdk():
    """Phase 2: Test pyrtlsdr Python library."""
    print("\n" + "=" * 60)
    print("PHASE 2: Python SDK (pyrtlsdr)")
    print("=" * 60)
    try:
        from rtlsdr import RtlSdr
    except ImportError:
        print("  [FAIL] pyrtlsdr not installed. Run: pip install pyrtlsdr[lib]")
        return False

    try:
        sdr = RtlSdr()
        print(f"  Tuner type:       {sdr.get_tuner_type()}")
        print(f"  Available gains:  {sdr.get_gains()}")
        print(f"  Sample rate:      {sdr.sample_rate / 1e6:.1f} MHz")
        print(f"  Center freq:      {sdr.center_freq / 1e6:.1f} MHz")

        # Quick capture test — 1024 samples at 100.3 MHz FM
        sdr.sample_rate = 2.048e6
        sdr.center_freq = 100.3e6
        sdr.gain = 'auto'
        samples = sdr.read_samples(1024)
        sdr.close()

        print(f"  Captured samples: {len(samples)}")
        print(f"  Sample dtype:     {samples.dtype}")
        print(f"  Mean power:       {abs(samples).mean():.4f}")
        print("  [OK] Python SDK working!")
        return True
    except Exception as e:
        print(f"  [FAIL] {e}")
        return False


def test_spectrum_scan():
    """Phase 3: Quick spectrum power scan (FM band snippet)."""
    print("\n" + "=" * 60)
    print("PHASE 3: Spectrum Scan (rtl_power)")
    print("=" * 60)
    # Scan a 2 MHz slice of FM band for 2 seconds
    output = run_cli_tool(
        "rtl_power",
        ["-f", "100M:102M:100k", "-i", "1", "-1"],
        timeout=15
    )
    if output is None:
        return False
    lines = [l for l in output.strip().split("\n") if l and not l.startswith("[")]
    if lines:
        print(f"  Got {len(lines)} scan line(s)")
        print(f"  Sample: {lines[0][:100]}...")
        print("  [OK] Spectrum scan working!")
        return True
    else:
        print("  [FAIL] No scan data returned")
        print(output)
        return False


if __name__ == "__main__":
    print("RTL-SDR Device Validation")
    print(f"Tools dir: {TOOLS_DIR}")
    print()

    results = {}
    results["detection"] = test_device_detection()
    if results["detection"]:
        results["python_sdk"] = test_python_sdk()
        results["spectrum"] = test_spectrum_scan()
    else:
        results["python_sdk"] = False
        results["spectrum"] = False

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for test, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {test}")

    all_pass = all(results.values())
    print(f"\n{'All tests passed! SDR is ready for agent use.' if all_pass else 'Some tests failed — see details above.'}")
    sys.exit(0 if all_pass else 1)
