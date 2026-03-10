#!/bin/bash
PASS="Mousepad7"
HOST="172.16.42.1"

echo "=== Restarting Go daemon and full verification ==="
sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@$HOST bash <<'REMOTECMD'
echo "[1] Restart the Go daemon (/pineapple/pineapple) via init..."
/etc/init.d/pineapple restart 2>&1
sleep 3
echo ""

echo "[2] Verify both processes are running:"
pgrep -a pineapd
pgrep -a pineapple
echo ""

echo "[3] Check the API from localhost with auth attempt:"
curl -s --connect-timeout 3 http://127.0.0.1:1471/api/pineap/settings 2>&1
echo ""
echo ""

echo "[4] Wait 15s for collection..."
sleep 15
echo ""

echo "[5] Check for pineap.log:"
ls -la /tmp/pineap.log 2>&1
if [ -f /tmp/pineap.log ]; then
    echo "Line count:"
    wc -l /tmp/pineap.log
    echo "Last 10 lines:"
    tail -10 /tmp/pineap.log
fi
echo ""

echo "[6] Check recon.db:"
sqlite3 /root/recon.db "SELECT count(*) FROM aps;" 2>/dev/null
echo " APs in recon.db"
sqlite3 /root/recon.db "SELECT ssid FROM aps ORDER BY last_seen DESC LIMIT 10;" 2>/dev/null
echo ""

echo "[7] Check SSID pool:"
wc -l /etc/pineapple/ssid_pool 2>/dev/null
head -20 /etc/pineapple/ssid_pool 2>/dev/null
echo ""

echo "[8] Check pineapple.db SSIDs (the Go daemon's DB):"
sqlite3 /pineapple/pineapple.db ".tables" 2>/dev/null
sqlite3 /pineapple/pineapple.db "SELECT name FROM sqlite_master WHERE type='table';" 2>/dev/null
echo ""

echo "[9] wlan1mon current channel (is it hopping?):"
for i in 1 2 3 4 5; do
    sleep 1
    iw dev wlan1mon info 2>/dev/null | grep channel
done
echo ""

echo "=== FULL VERIFY DONE ==="
REMOTECMD
