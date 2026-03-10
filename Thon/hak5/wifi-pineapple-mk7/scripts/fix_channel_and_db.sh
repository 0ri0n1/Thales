#!/bin/bash
PASS="Mousepad7"
HOST="172.16.42.1"

echo "=== Channel hopping and DB investigation ==="
sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@$HOST bash <<'REMOTECMD'
echo "[1] Check pineapd_wrapper for channel hop logic:"
cat /usr/sbin/pineapd_wrapper 2>/dev/null
echo "---END---"
echo ""

echo "[2] Check pineapd help/usage:"
/usr/sbin/pineapd --help 2>&1 | head -20
echo ""

echo "[3] recon.db structure:"
sqlite3 /root/recon.db ".schema" 2>/dev/null
echo ""

echo "[4] log.db structure:"
sqlite3 /root/log.db ".schema" 2>/dev/null
echo ""

echo "[5] pineapple.db structure:"
sqlite3 /pineapple/pineapple.db ".schema" 2>/dev/null
echo ""

echo "[6] /etc/pineapple/pineapple.db structure:"
sqlite3 /etc/pineapple/pineapple.db ".schema" 2>/dev/null
echo ""

echo "[7] Check /etc/pineapple/ for SSID pool and config files:"
ls -la /etc/pineapple/ 2>/dev/null
echo ""

echo "[8] Check if ssid_pool file exists or if SSIDs are in DB:"
cat /etc/pineapple/ssid_pool 2>/dev/null | wc -l
sqlite3 /etc/pineapple/pineapple.db "SELECT name FROM sqlite_master WHERE type='table';" 2>/dev/null
sqlite3 /etc/pineapple/pineapple.db "SELECT count(*) as cnt, 'ssids' as tbl FROM ssids UNION ALL SELECT count(*), 'pool' FROM pool;" 2>/dev/null
echo ""

echo "[9] Manual channel hop test (does the radio respond?):"
echo "Setting ch1..."
iw dev wlan1mon set channel 1 2>&1
sleep 0.5
iw dev wlan1mon info 2>/dev/null | grep channel
echo "Setting ch6..."
iw dev wlan1mon set channel 6 2>&1
sleep 0.5
iw dev wlan1mon info 2>/dev/null | grep channel
echo "Setting ch11..."
iw dev wlan1mon set channel 11 2>&1
sleep 0.5
iw dev wlan1mon info 2>/dev/null | grep channel
echo ""

echo "[10] pineapd strace (2 seconds of syscalls):"
PINEAPD_PID=$(pidof pineapd)
if [ -n "$PINEAPD_PID" ]; then
    strace -p $PINEAPD_PID -e trace=write,open,openat,ioctl -f -t 2>&1 &
    STRACE_PID=$!
    sleep 2
    kill $STRACE_PID 2>/dev/null
    wait $STRACE_PID 2>/dev/null
fi
echo ""

echo "=== DONE ==="
REMOTECMD
