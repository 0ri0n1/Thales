#!/bin/bash
export SSHPASS=Mousepad7
SSH="sshpass -e ssh -o StrictHostKeyChecking=no root@172.16.42.1"
SCP="sshpass -e scp -o StrictHostKeyChecking=no"

echo "[1] Pulling filters.db..."
$SCP root@172.16.42.1:/etc/pineapple/filters.db /tmp/filters.db

echo "[2] Current deny list:"
sqlite3 /tmp/filters.db "SELECT * FROM mac_filter_list;"
echo "---"

echo "[3] Adding 5 new MACs..."
sqlite3 /tmp/filters.db "INSERT OR IGNORE INTO mac_filter_list (mac) VALUES ('D8:A0:11:72:49:DC');"
sqlite3 /tmp/filters.db "INSERT OR IGNORE INTO mac_filter_list (mac) VALUES ('CC:40:85:CF:44:8C');"
sqlite3 /tmp/filters.db "INSERT OR IGNORE INTO mac_filter_list (mac) VALUES ('48:E1:E9:42:E9:CC');"
sqlite3 /tmp/filters.db "INSERT OR IGNORE INTO mac_filter_list (mac) VALUES ('48:E1:E9:42:E9:69');"
sqlite3 /tmp/filters.db "INSERT OR IGNORE INTO mac_filter_list (mac) VALUES ('0C:EF:AF:CE:68:1E');"

echo "[4] Updated deny list:"
sqlite3 /tmp/filters.db "SELECT * FROM mac_filter_list;"
echo "---"

echo "[5] Pushing back to Pineapple..."
$SCP /tmp/filters.db root@172.16.42.1:/etc/pineapple/filters.db

echo "[6] Verifying on Pineapple..."
$SSH "sqlite3 /etc/pineapple/filters.db 'SELECT count(*) FROM mac_filter_list;'"

echo "[DONE] Deny list updated."
