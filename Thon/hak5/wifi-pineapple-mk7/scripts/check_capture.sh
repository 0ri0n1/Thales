#!/bin/bash
PASS="Mousepad7"
HOST="172.16.42.1"

echo "=== Copy DBs and check capture from Kali ==="

echo "[1] SCP recon.db from Pineapple..."
sshpass -p "$PASS" scp -o StrictHostKeyChecking=no root@$HOST:/root/recon.db /tmp/pineapple_recon.db 2>&1
echo "Exit: $?"
echo ""

echo "[2] SCP log.db from Pineapple..."
sshpass -p "$PASS" scp -o StrictHostKeyChecking=no root@$HOST:/root/log.db /tmp/pineapple_log.db 2>&1
echo "Exit: $?"
echo ""

echo "[3] SCP /etc/pineapple/pineapple.db..."
sshpass -p "$PASS" scp -o StrictHostKeyChecking=no root@$HOST:/etc/pineapple/pineapple.db /tmp/pineapple_etc.db 2>&1
echo "Exit: $?"
echo ""

echo "[4] SCP /etc/pineapple/filters.db..."
sshpass -p "$PASS" scp -o StrictHostKeyChecking=no root@$HOST:/etc/pineapple/filters.db /tmp/pineapple_filters.db 2>&1
echo "Exit: $?"
echo ""

echo "[5] SCP /etc/pineapple/pineape.db..."
sshpass -p "$PASS" scp -o StrictHostKeyChecking=no root@$HOST:/etc/pineapple/pineape.db /tmp/pineapple_pineape.db 2>&1
echo "Exit: $?"
echo ""

echo "[6] Analyze recon.db:"
sqlite3 /tmp/pineapple_recon.db ".tables" 2>&1
sqlite3 /tmp/pineapple_recon.db ".schema" 2>&1
sqlite3 /tmp/pineapple_recon.db "SELECT count(*) || ' APs' FROM aps;" 2>/dev/null
sqlite3 /tmp/pineapple_recon.db "SELECT count(*) || ' clients' FROM clients;" 2>/dev/null
sqlite3 /tmp/pineapple_recon.db "SELECT ssid, bssid, last_seen FROM aps ORDER BY last_seen DESC LIMIT 10;" 2>/dev/null
echo ""

echo "[7] Analyze log.db:"
sqlite3 /tmp/pineapple_log.db ".tables" 2>&1
sqlite3 /tmp/pineapple_log.db ".schema" 2>&1
sqlite3 /tmp/pineapple_log.db "SELECT count(*) || ' entries' FROM log;" 2>/dev/null
sqlite3 /tmp/pineapple_log.db "SELECT * FROM log ORDER BY rowid DESC LIMIT 5;" 2>/dev/null
echo ""

echo "[8] Analyze pineapple.db:"
sqlite3 /tmp/pineapple_etc.db ".tables" 2>&1
sqlite3 /tmp/pineapple_etc.db ".schema" 2>&1
echo ""

echo "[9] Analyze pineape.db:"
sqlite3 /tmp/pineapple_pineape.db ".tables" 2>&1
sqlite3 /tmp/pineapple_pineape.db ".schema" 2>&1
echo ""

echo "[10] Analyze filters.db:"
sqlite3 /tmp/pineapple_filters.db ".tables" 2>&1
sqlite3 /tmp/pineapple_filters.db ".schema" 2>&1
sqlite3 /tmp/pineapple_filters.db "SELECT count(*) || ' mac filters' FROM mac_filter_list;" 2>/dev/null
sqlite3 /tmp/pineapple_filters.db "SELECT count(*) || ' ssid filters' FROM ssid_filter_list;" 2>/dev/null
sqlite3 /tmp/pineapple_filters.db "SELECT * FROM mac_filter_list;" 2>/dev/null
sqlite3 /tmp/pineapple_filters.db "SELECT * FROM ssid_filter_list;" 2>/dev/null
echo ""

echo "=== DONE ==="
