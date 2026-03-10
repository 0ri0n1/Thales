#!/bin/bash
export SSHPASS=Mousepad7
SSH="sshpass -e ssh -o StrictHostKeyChecking=no root@172.16.42.1"
SCP="sshpass -e scp -o StrictHostKeyChecking=no"

echo "=== CLEANUP & ADD LEPRO MAC ==="

echo "[1] Disabling PineAP beacon responses and broadcast..."
$SSH "uci set pineap.@config[0].beacon_responses=off && uci set pineap.@config[0].capture_ssids=off && uci set pineap.@config[0].broadcast_ssid_pool=off && uci set pineap.@config[0].logging=off && uci commit pineap"

echo "[2] Killing airodump and tcpdump..."
$SSH "killall airodump-ng 2>/dev/null; killall tcpdump 2>/dev/null"

echo "[3] Removing TELUS5434 from SSID pool..."
$SSH "sed -i '/TELUS5434/d' /etc/pineapple/ssid_pool.txt; cat /etc/pineapple/ssid_pool.txt"

echo "[4] Adding Lepro MAC to deny list..."
$SCP root@172.16.42.1:/etc/pineapple/filters.db /tmp/filters.db
sqlite3 /tmp/filters.db "INSERT OR IGNORE INTO mac_filter_list (mac) VALUES ('70:89:76:25:FB:B3');"
echo "Updated deny list:"
sqlite3 /tmp/filters.db "SELECT * FROM mac_filter_list;"

echo "[5] Pushing updated filters.db back..."
$SCP /tmp/filters.db root@172.16.42.1:/etc/pineapple/filters.db

echo "[6] Final PineAP state:"
$SSH "uci show pineap | grep -E 'beacon|capture|broadcast|logging|karma'"

echo "[7] Deny list count:"
sqlite3 /tmp/filters.db "SELECT count(*) FROM mac_filter_list;"

echo "=== DONE ==="
