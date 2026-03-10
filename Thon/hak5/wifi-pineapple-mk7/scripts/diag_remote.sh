#!/bin/bash
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@172.16.42.1 bash <<'REMOTECMD'
echo "=== BASIC INFO ==="
echo "CONNECTED"
uptime
cat /etc/openwrt_release 2>/dev/null
echo ""

echo "=== DISK SPACE ==="
df -h /tmp /overlay 2>/dev/null
echo ""

echo "=== PROCESSES ==="
ps w 2>/dev/null
echo ""

echo "=== IWCONFIG ==="
iwconfig 2>&1
echo ""

echo "=== IW DEV ==="
iw dev 2>&1
echo ""

echo "=== PINEAP LOG ==="
ls -la /tmp/pineap* 2>&1
echo ""
wc -l /tmp/pineap.log 2>/dev/null
echo ""

echo "=== HARVEST DIR ==="
ls -la /tmp/ssid_harvest/ 2>&1
echo ""

echo "=== PINEAPPLE DIR ==="
ls -la /pineapple/ 2>&1
echo ""

echo "=== PINEAPPLE DAEMON STATUS ==="
pgrep -a pineapple 2>/dev/null
echo "pineapple_procs=$?"
echo ""

echo "=== PINEAP CONFIG ==="
uci show pineap 2>/dev/null
echo ""

echo "=== WLAN1 MONITOR CHECK ==="
iwconfig wlan1mon 2>&1
iwconfig wlan1 2>&1
echo ""

echo "=== WLAN2 STATUS ==="
iwinfo wlan2 info 2>&1
echo ""

echo "=== HOSTAPD CHECK ==="
pgrep -a hostapd 2>/dev/null
echo "hostapd_procs=$?"
echo ""

echo "=== DMESG WIFI ERRORS (last 20) ==="
dmesg 2>/dev/null | grep -iE 'wlan|wifi|ieee|ath|mt76|firmware|error|fail' | tail -20
echo ""

echo "=== DIAG COMPLETE ==="
REMOTECMD
