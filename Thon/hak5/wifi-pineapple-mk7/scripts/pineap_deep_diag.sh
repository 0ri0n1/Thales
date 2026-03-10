#!/bin/bash
PASS="Mousepad7"
HOST="172.16.42.1"

echo "=== Deep PineAP diagnostic ==="
sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@$HOST bash <<'REMOTECMD'
echo "[1] PineAP conf file (runtime config):"
cat /tmp/pineap.conf 2>/dev/null
echo ""
echo "---"
echo ""

echo "[2] PineAP socket:"
ls -la /tmp/pineapple.sock 2>&1
echo ""

echo "[3] All /tmp/pineap* files:"
ls -la /tmp/pineap* 2>&1
find /tmp -name "*pineap*" -o -name "*ssid*" -o -name "*probe*" 2>/dev/null
echo ""

echo "[4] Daemon open files:"
ls -la /proc/5458/fd/ 2>/dev/null | head -30
echo ""

echo "[5] Check if pineapple.db has SSIDs:"
sqlite3 /pineapple/pineapple.db ".tables" 2>/dev/null
echo ""
sqlite3 /pineapple/pineapple.db "SELECT count(*) FROM ssids;" 2>/dev/null
echo ""
sqlite3 /etc/pineapple/pineapple.db ".tables" 2>/dev/null
echo ""
sqlite3 /etc/pineapple/pineapple.db "SELECT count(*) FROM ssids;" 2>/dev/null
echo ""

echo "[6] Checking if pineapple daemon reads pineap.conf or UCI:"
strings /pineapple/pineapple 2>/dev/null | grep -iE 'pineap.conf|uci|capture_ssid|logging|beacon_resp' | head -20
echo ""

echo "[7] API test from localhost:"
curl -s --connect-timeout 3 http://127.0.0.1:1471/api/pineap/settings 2>&1
echo ""
echo ""

echo "[8] Try enabling via API (POST):"
curl -s --connect-timeout 3 -X PUT http://127.0.0.1:1471/api/pineap/settings \
  -H "Content-Type: application/json" \
  -d '{"settings":{"enablePineAP":true,"beacon_responses":true,"capture_ssids":true,"broadcast_ssid_pool":true,"logging":true,"beacon_interval":"AGGRESSIVE","beacon_response_interval":"NORMAL","target_mac":"FF:FF:FF:FF:FF:FF","karma":false}}' 2>&1
echo ""
echo ""

echo "[9] Check pineap.conf content again:"
cat /tmp/pineap.conf 2>/dev/null
echo ""

echo "[10] Any log files now?"
ls -la /tmp/pineap* 2>&1
echo ""

echo "=== DEEP DIAG DONE ==="
REMOTECMD
