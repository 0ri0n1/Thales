#!/bin/bash
echo "=== Final collection verification ==="

echo "[1] SSID pool in pineapple.db:"
sqlite3 /tmp/pineapple_etc.db "SELECT count(*) || ' SSIDs in pool' FROM ssids;" 2>/dev/null
sqlite3 /tmp/pineapple_etc.db "SELECT ssid FROM ssids ORDER BY created_at DESC LIMIT 30;" 2>/dev/null
echo ""

echo "[2] Recent probes from log.db (last 20 unique SSIDs):"
sqlite3 /tmp/pineapple_log.db "SELECT DISTINCT ssid FROM log WHERE ssid != '' ORDER BY updated_at DESC LIMIT 20;" 2>/dev/null
echo ""

echo "[3] Total unique probed SSIDs:"
sqlite3 /tmp/pineapple_log.db "SELECT count(DISTINCT ssid) || ' unique probed SSIDs' FROM log WHERE ssid != '';" 2>/dev/null
echo ""

echo "[4] Recent AP SSIDs from recon.db:"
sqlite3 /tmp/pineapple_recon.db "SELECT ssid, channel, encryption, signal, last_seen FROM aps WHERE ssid != '' ORDER BY last_seen DESC LIMIT 20;" 2>/dev/null
echo ""

echo "[5] Scan IDs (recon runs):"
sqlite3 /tmp/pineapple_recon.db "SELECT * FROM scan_ids ORDER BY date DESC LIMIT 5;" 2>/dev/null
echo ""

echo "[6] Probe log entries in last 5 minutes (log_type 0 = probe):"
NOW=$(date +%s)
FIVE_AGO=$((NOW - 300))
sqlite3 /tmp/pineapple_log.db "SELECT count(*) || ' entries in last 5 min' FROM log WHERE updated_at > $FIVE_AGO;" 2>/dev/null
echo ""

echo "[7] Most active probing clients (top 10):"
sqlite3 /tmp/pineapple_log.db "SELECT mac, count(*) as cnt, GROUP_CONCAT(DISTINCT ssid) as probed_ssids FROM log WHERE ssid != '' GROUP BY mac ORDER BY cnt DESC LIMIT 10;" 2>/dev/null
echo ""

echo "=== DONE ==="
