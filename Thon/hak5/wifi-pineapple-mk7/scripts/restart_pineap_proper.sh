#!/bin/bash
PASS="Mousepad7"
HOST="172.16.42.1"

echo "=== Proper PineAP restart with UCI config applied ==="
sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@$HOST bash <<'REMOTECMD'
echo "[1] Confirm UCI config is correct:"
uci get pineap.@config[0].capture_ssids
uci get pineap.@config[0].broadcast_ssid_pool
uci get pineap.@config[0].beacon_responses
uci get pineap.@config[0].logging
echo ""

echo "[2] Kill ALL pineapple processes..."
killall -9 pineapple 2>/dev/null
sleep 1
killall -9 pineapd 2>/dev/null
sleep 1
echo "Killed. Process check:"
pgrep -a pineap
echo ""

echo "[3] Remove stale runtime config so daemon regenerates from UCI..."
rm -f /tmp/pineap.conf
echo "Removed /tmp/pineap.conf"
echo ""

echo "[4] Check for init scripts..."
ls -la /etc/init.d/pineap* 2>&1
ls -la /etc/init.d/pineapple* 2>&1
echo ""

echo "[5] Try init.d restart first..."
if [ -x /etc/init.d/pineapd ]; then
    /etc/init.d/pineapd restart 2>&1
    echo "Used /etc/init.d/pineapd restart"
elif [ -x /etc/init.d/pineapple ]; then
    /etc/init.d/pineapple restart 2>&1
    echo "Used /etc/init.d/pineapple restart"
else
    echo "No init script found, starting manually..."
    /pineapple/pineapple &
    echo "Started /pineapple/pineapple manually"
fi
sleep 3
echo ""

echo "[6] Verify daemon is running:"
pgrep -a pineap
echo ""

echo "[7] Check regenerated pineap.conf:"
cat /tmp/pineap.conf 2>/dev/null
echo ""

echo "[8] Wait 5s for log creation..."
sleep 5
echo "pineap files after wait:"
ls -la /tmp/pineap* 2>&1
echo ""

echo "=== RESTART DONE ==="
REMOTECMD

echo "SSH exit: $?"
