#!/bin/bash
PASS="Mousepad7"
HOST="172.16.42.1"

echo "=== pineapd deep investigation ==="
sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@$HOST bash <<'REMOTECMD'
echo "[1] All pineap-related processes:"
ps w | grep -E 'pineap|pineapple'
echo ""

echo "[2] pineapd binary details:"
ls -la /usr/sbin/pineapd 2>&1
file /usr/sbin/pineapd 2>/dev/null
echo ""

echo "[3] pineapd_wrapper init script:"
cat /etc/init.d/pineapd 2>/dev/null
echo ""

echo "[4] pineapple init script:"
cat /etc/init.d/pineapple 2>/dev/null
echo ""

echo "[5] pineapd FDs (actual pineapd PID):"
PINEAPD_PID=$(pidof pineapd)
echo "pineapd PID: $PINEAPD_PID"
if [ -n "$PINEAPD_PID" ]; then
    ls -la /proc/$PINEAPD_PID/fd/ 2>/dev/null
fi
echo ""

echo "[6] /pineapple/pineapple FDs (Go daemon):"
GO_PID=$(pidof pineapple)
echo "pineapple PID: $GO_PID"
if [ -n "$GO_PID" ]; then
    ls -la /proc/$GO_PID/fd/ 2>/dev/null
fi
echo ""

echo "[7] Check pineapd socket communication:"
ls -la /tmp/run/pineapd.sock 2>&1
echo ""

echo "[8] Quick raw capture test (3s of probe requests via pineapd interface):"
tcpdump -i wlan1mon -c 5 'subtype probe-req' 2>&1 &
TCPD_PID=$!
sleep 4
kill $TCPD_PID 2>/dev/null
wait $TCPD_PID 2>/dev/null
echo ""

echo "[9] Check if pineap logging writes to syslog instead:"
logread 2>/dev/null | grep -iE 'ssid|probe|pineap.*log|capture' | tail -20
echo ""

echo "[10] Check recon.db for any captures:"
if [ -f /root/recon.db ]; then
    sqlite3 /root/recon.db ".tables" 2>/dev/null
    echo "APs count:"
    sqlite3 /root/recon.db "SELECT count(*) FROM aps;" 2>/dev/null
    echo "Clients count:"
    sqlite3 /root/recon.db "SELECT count(*) FROM clients;" 2>/dev/null
    echo "Recent APs:"
    sqlite3 /root/recon.db "SELECT ssid,bssid,last_seen FROM aps ORDER BY last_seen DESC LIMIT 10;" 2>/dev/null
else
    echo "No recon.db found"
fi
echo ""

echo "[11] Check log.db (hostapd):"
if [ -f /root/log.db ]; then
    sqlite3 /root/log.db ".tables" 2>/dev/null
    sqlite3 /root/log.db "SELECT count(*) FROM log;" 2>/dev/null 
    echo "Recent entries:"
    sqlite3 /root/log.db "SELECT * FROM log ORDER BY rowid DESC LIMIT 5;" 2>/dev/null
else
    echo "No log.db found"
fi
echo ""

echo "=== DEEP DONE ==="
REMOTECMD
