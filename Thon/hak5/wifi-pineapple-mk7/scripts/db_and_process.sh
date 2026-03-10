#!/bin/bash
PASS="Mousepad7"
HOST="172.16.42.1"

echo "=== DB integrity and process state ==="
sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@$HOST bash <<'REMOTECMD'
echo "[1] pineapd process alive check:"
PINEAPD_PID=$(pidof pineapd)
echo "PID: $PINEAPD_PID"
if [ -n "$PINEAPD_PID" ]; then
    cat /proc/$PINEAPD_PID/status 2>/dev/null | head -5
    echo "FDs:"
    ls -la /proc/$PINEAPD_PID/fd/ 2>/dev/null
fi
echo ""

echo "[2] DB integrity checks:"
for db in /root/recon.db /root/log.db /pineapple/pineapple.db /etc/pineapple/pineapple.db /etc/pineapple/pineape.db /etc/pineapple/filters.db /etc/pineapple/previous_clients.db; do
    echo "--- $db ---"
    if [ -f "$db" ]; then
        size=$(ls -la "$db" | awk '{print $5}')
        echo "  Size: $size bytes"
        sqlite3 "$db" "PRAGMA integrity_check;" 2>&1
        tables=$(sqlite3 "$db" "SELECT name FROM sqlite_master WHERE type='table';" 2>&1)
        echo "  Tables: $tables"
        if [ -n "$tables" ]; then
            for t in $tables; do
                cnt=$(sqlite3 "$db" "SELECT count(*) FROM $t;" 2>/dev/null)
                echo "  $t: $cnt rows"
            done
        fi
    else
        echo "  NOT FOUND"
    fi
    echo ""
done

echo "[3] Check pineapd stderr output (what did it log at startup?):"
logread 2>/dev/null | grep -i pineapd | tail -10
echo ""

echo "[4] Check if pineapd writes to stdout (procd captures):"
logread 2>/dev/null | grep -E 'pineapd|CONFIG|SSID|capture|beacon' | tail -20
echo ""

echo "[5] pineap_mode content:"
cat /etc/pineapple/pineap_mode 2>/dev/null
echo ""

echo "[6] version:"
cat /etc/pineapple/version 2>/dev/null
echo ""

echo "=== DONE ==="
REMOTECMD
