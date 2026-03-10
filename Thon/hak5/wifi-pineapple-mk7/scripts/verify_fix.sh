#!/bin/bash
echo "=== Verifying PineAP fix ==="

echo "[1] Testing key-based SSH..."
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 -o IdentitiesOnly=yes -i /root/.ssh/id_ed25519 root@172.16.42.1 'echo KEY_AUTH_OK' 2>/dev/null
echo "Key auth exit: $?"
echo ""

echo "[2] Checking PineAP state via password SSH..."
sshpass -p "Mousepad7" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@172.16.42.1 bash <<'REMOTECMD'
echo "--- PineAP daemon ---"
pgrep -a pineapple
echo ""

echo "--- PineAP config (collection features) ---"
uci get pineap.@config[0].capture_ssids
uci get pineap.@config[0].broadcast_ssid_pool
uci get pineap.@config[0].beacon_responses
uci get pineap.@config[0].logging
echo ""

echo "--- pineap.log check ---"
ls -la /tmp/pineap.log 2>&1
wc -l /tmp/pineap.log 2>/dev/null
echo ""
echo "--- Last 10 log entries ---"
tail -10 /tmp/pineap.log 2>/dev/null
echo ""

echo "--- SSID pool check ---"
wc -l /etc/pineapple/ssid_pool 2>/dev/null
echo ""
echo "--- Pool contents (first 10) ---"
head -10 /etc/pineapple/ssid_pool 2>/dev/null
echo ""

echo "--- Active connections ---"
iwinfo wlan0 assoclist 2>/dev/null
iwinfo wlan0-1 assoclist 2>/dev/null
echo ""

echo "--- wlan1mon status ---"
iwconfig wlan1mon 2>&1
echo ""

echo "=== VERIFY DONE ==="
REMOTECMD
