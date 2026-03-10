#!/bin/bash
PASS="Mousepad7"
HOST="172.16.42.1"

echo "=== Fixing monitor interface and channel hopping ==="
sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@$HOST bash <<'REMOTECMD'
echo "[1] Current interface state:"
iw dev
echo ""

echo "[2] wlan1 and wlan1mon both exist on phy1 - checking for conflict..."
echo "wlan1 type:"
iw dev wlan1 info 2>&1 | grep type
echo "wlan1mon type:"
iw dev wlan1mon info 2>&1 | grep type
echo ""

echo "[3] Stopping pineapd to clean up interfaces..."
/etc/init.d/pineapd stop 2>&1
sleep 2
killall -9 pineapd 2>/dev/null
sleep 1
echo "pineapd stopped"
echo ""

echo "[4] Removing duplicate monitor interface (wlan1mon)..."
iw wlan1mon del 2>/dev/null
echo "wlan1mon removed"
echo ""

echo "[5] Verifying wlan1 is in monitor mode..."
iw dev wlan1 info 2>&1 | grep type
echo ""

echo "[6] If wlan1 is still monitor, recreate wlan1mon cleanly..."
iw dev wlan1 info 2>&1 | grep "type monitor"
if [ $? -eq 0 ]; then
    echo "wlan1 is already in monitor mode, setting wlan1 back to managed first..."
    ip link set wlan1 down 2>/dev/null
    iw wlan1 set type managed 2>/dev/null
    ip link set wlan1 up 2>/dev/null
    sleep 1
fi

echo "[7] Create fresh wlan1mon via airmon-ng..."
airmon-ng start wlan1 2>&1
sleep 2
echo ""

echo "[8] New interface state:"
iw dev
echo ""

echo "[9] Verify monitor interface packet reception (quick test)..."
ifconfig wlan1mon 2>/dev/null | grep "RX packets"
echo ""

echo "[10] Restart pineapd with clean config..."
rm -f /tmp/pineap.conf
/etc/init.d/pineapd restart 2>&1
sleep 3
echo ""

echo "[11] Verify processes:"
pgrep -a pineapd
pgrep -a pineapple
echo ""

echo "[12] New pineap.conf content (key lines):"
grep -E 'beacon_responses|capture_ssids|broadcast_ssid_pool|logging|pineap_interface' /tmp/pineap.conf 2>/dev/null
echo ""

echo "[13] Wait 10s for probes..."
sleep 10
echo ""

echo "[14] Check for pineap.log:"
ls -la /tmp/pineap.log 2>&1
echo ""

echo "[15] Quick tcpdump (any management frames, 3s):"
tcpdump -i wlan1mon -c 5 'type mgt' -e 2>&1 &
TCPD_PID=$!
sleep 4
kill $TCPD_PID 2>/dev/null
wait $TCPD_PID 2>/dev/null
echo ""

echo "[16] wlan1mon RX packets now:"
ifconfig wlan1mon 2>/dev/null | grep "RX packets"
echo ""

echo "=== MONITOR FIX DONE ==="
REMOTECMD
