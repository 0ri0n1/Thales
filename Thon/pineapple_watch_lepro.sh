#!/bin/bash
export SSHPASS=Mousepad7
SSH="sshpass -e ssh -o StrictHostKeyChecking=no root@172.16.42.1"

echo "=== WATCHING FOR LEPRO (70:89:76:25:FB:B3) ==="

echo "[1] Quick airodump on Ch11 (20s)..."
$SSH "killall airodump-ng 2>/dev/null; airodump-ng wlan1mon -c 11 --write /tmp/lepro_watch --output-format csv &>/dev/null & sleep 20; killall airodump-ng 2>/dev/null; sleep 1"

echo "[2] All stations seen:"
$SSH "cat /tmp/lepro_watch-01.csv 2>/dev/null | grep -A999 'Station MAC'"

echo ""
echo "[3] Lepro specifically:"
$SSH "cat /tmp/lepro_watch-01.csv 2>/dev/null | grep -i '70:89:76'"

echo ""
echo "[4] Probe requests (tcpdump 15s)..."
$SSH "timeout 15 tcpdump -i wlan1mon -e -n 'type mgt subtype probe-req' 2>/dev/null | grep -i '70:89:76' || echo 'No Lepro probes seen in 15s'"

echo ""
echo "[5] All probe requests in last 15s:"
$SSH "timeout 15 tcpdump -i wlan1mon -e -n 'type mgt subtype probe-req' 2>/dev/null | head -30"

echo ""
echo "[6] PineAP recon DB - recent clients:"
$SSH "strings /root/recon.db 2>/dev/null | grep -i '70:89:76' || echo 'Not in recon.db'"

echo ""
echo "[7] Cleanup..."
$SSH "rm -f /tmp/lepro_watch-01.* 2>/dev/null"

echo "=== DONE ==="
