#!/bin/bash
PASS="Mousepad7"
HOST="172.16.42.1"

echo "=== Fixing PineAP config via UCI (bypassing broken web UI) ==="
sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@$HOST bash <<'REMOTECMD'
echo "[1/6] Current PineAP config (BEFORE):"
uci show pineap 2>/dev/null
echo ""

echo "[2/6] Enabling PineAP collection features..."
uci set pineap.@config[0].capture_ssids='on'
uci set pineap.@config[0].broadcast_ssid_pool='on'
uci set pineap.@config[0].beacon_responses='on'
uci set pineap.@config[0].logging='on'
uci set pineap.@config[0].beacon_interval='AGGRESSIVE'
uci set pineap.@config[0].beacon_response_interval='NORMAL'
uci set pineap.@config[0].target_mac='FF:FF:FF:FF:FF:FF'
uci set pineap.@config[0].autostart='on'
uci commit pineap
echo "UCI commit done."
echo ""

echo "[3/6] Restarting PineAP daemon to pick up new config..."
killall pineapple 2>/dev/null
sleep 2
/pineapple/pineapple &
sleep 3
echo ""

echo "[4/6] Verifying daemon is running..."
pgrep -a pineapple
echo ""

echo "[5/6] Config (AFTER):"
uci show pineap 2>/dev/null
echo ""

echo "[6/6] Checking for pineap.log creation..."
sleep 5
ls -la /tmp/pineap* 2>&1
echo ""

echo "=== FIX COMPLETE ==="
REMOTECMD

echo ""
echo "SSH exit: $?"
