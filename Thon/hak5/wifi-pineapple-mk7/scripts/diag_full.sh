#!/bin/bash
PASS="Mousepad7"
HOST="172.16.42.1"

echo "=== Testing SSH with known password ==="
sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@$HOST bash <<'REMOTECMD'
echo "=== BASIC INFO ==="
echo "CONNECTED SUCCESSFULLY"
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
echo "--- pineap.log line count ---"
wc -l /tmp/pineap.log 2>/dev/null
echo ""
echo "--- Last 10 pineap.log entries ---"
tail -10 /tmp/pineap.log 2>/dev/null
echo ""

echo "=== HARVEST DIR ==="
ls -la /tmp/ssid_harvest/ 2>&1
echo ""
echo "--- Master SSID count ---"
wc -l /tmp/ssid_harvest/ssid_master.txt 2>/dev/null
echo ""

echo "=== PINEAPPLE DIR ==="
ls -la /pineapple/ 2>&1
echo ""

echo "=== PINEAPPLE DAEMON ==="
pgrep -a pineapple 2>/dev/null
echo "pineapple_exit=$?"
echo ""

echo "=== HOSTAPD ==="
pgrep -a hostapd 2>/dev/null
echo "hostapd_exit=$?"
echo ""

echo "=== WLAN INTERFACES ==="
echo "--- wlan0 ---"
iwinfo wlan0 info 2>&1
echo ""
echo "--- wlan1 ---"
iwinfo wlan1 info 2>&1
echo ""
echo "--- wlan1mon ---"
iwconfig wlan1mon 2>&1
echo ""
echo "--- wlan2 ---"
iwinfo wlan2 info 2>&1
echo ""

echo "=== PINEAP UCI CONFIG ==="
uci show pineap 2>/dev/null
echo ""

echo "=== DMESG WIFI (last 30) ==="
dmesg 2>/dev/null | grep -iE 'wlan|wifi|ieee|mt76|firmware|error|fail|deauth' | tail -30
echo ""

echo "=== SSID POOL (first 20) ==="
cat /etc/pineapple/ssid_pool 2>/dev/null | head -20
echo ""
echo "Pool total:"
wc -l /etc/pineapple/ssid_pool 2>/dev/null
echo ""

echo "=== DIAG COMPLETE ==="
REMOTECMD

echo ""
echo "=== SSH Exit Code: $? ==="
