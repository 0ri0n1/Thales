#!/bin/bash
PASS="Mousepad7"
HOST="172.16.42.1"

echo "=== Verifying capture is active ==="
sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@$HOST bash <<'REMOTECMD'
echo "[1] pineapd process details:"
pgrep -a pineapd
echo ""

echo "[2] pineapd open files:"
PINEAPD_PID=$(pgrep -f '/usr/sbin/pineapd')
if [ -n "$PINEAPD_PID" ]; then
    ls -la /proc/$PINEAPD_PID/fd/ 2>/dev/null
fi
echo ""

echo "[3] wlan1mon stats (packet counts):"
ifconfig wlan1mon 2>&1
echo ""

echo "[4] Quick tcpdump test on wlan1mon (5 seconds, probe requests only):"
timeout 5 tcpdump -i wlan1mon -c 10 'type mgt subtype probe-req' -e 2>&1
echo ""

echo "[5] All files in /tmp with pineap in name:"
find /tmp -name '*pineap*' 2>/dev/null
echo ""

echo "[6] Check pineapd stderr (from procd):"
logread 2>/dev/null | grep -i pineap | tail -20
echo ""

echo "[7] pineap.log check:"
ls -la /tmp/pineap.log 2>&1
echo ""

echo "=== DONE ==="
REMOTECMD
