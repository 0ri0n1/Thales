#!/bin/bash
export SSHPASS=Mousepad7
SSH="sshpass -e ssh -o StrictHostKeyChecking=no root@172.16.42.1"

echo "=== LEPRO VERIFICATION ==="

echo "[1] Clients on wlan0 (management AP):"
$SSH "iwinfo wlan0 assoclist"

echo ""
echo "[2] Clients on wlan0-1 (open AP):"
$SSH "iwinfo wlan0-1 assoclist"

echo ""
echo "[3] ARP table:"
$SSH "cat /proc/net/arp"

echo ""
echo "[4] PineAP log (last 20 lines):"
$SSH "cat /var/log/pineap.log 2>/dev/null | tail -20; cat /root/log.db 2>/dev/null | strings | tail -20"

echo ""
echo "[5] airodump stations:"
$SSH "cat /tmp/lepro_hunt-01.csv 2>/dev/null"

echo ""
echo "[6] OUI lookup for 70:89:76:"
$SSH "python3 -c \"
import json
with open('/etc/pineapple/ouis') as f:
    oui = json.load(f)
print('708976:', oui.get('708976', 'UNKNOWN'))
\""

echo "=== DONE ==="
