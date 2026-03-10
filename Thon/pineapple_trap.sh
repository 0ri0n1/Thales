#!/bin/bash
export SSHPASS=Mousepad7
SSH="sshpass -e ssh -o StrictHostKeyChecking=no root@172.16.42.1"

echo "=== LEPRO BULB TRAP ==="

echo "[1] Setting wlan1mon to Channel 11..."
$SSH "iw dev wlan1mon set channel 11 2>/dev/null; iwinfo wlan1mon info 2>/dev/null | head -3"

echo "[2] Adding TELUS5434 to PineAP SSID pool..."
$SSH "echo TELUS5434 >> /etc/pineapple/ssid_pool.txt; sort -u /etc/pineapple/ssid_pool.txt -o /etc/pineapple/ssid_pool.txt; cat /etc/pineapple/ssid_pool.txt"

echo "[3] Enabling PineAP beacon responses + capture..."
$SSH "uci set pineap.@config[0].beacon_responses=on && uci set pineap.@config[0].capture_ssids=on && uci set pineap.@config[0].broadcast_ssid_pool=on && uci set pineap.@config[0].logging=on && uci commit pineap"

echo "[4] Verifying PineAP config..."
$SSH "uci show pineap"

echo "[5] Killing any old airodump..."
$SSH "killall airodump-ng 2>/dev/null; killall tcpdump 2>/dev/null; sleep 1"

echo "[6] Starting airodump-ng on Ch11 targeting TELUS5434..."
$SSH "airodump-ng wlan1mon -c 11 --bssid 10:78:5B:FA:3C:12 --write /tmp/lepro_hunt --output-format csv -w /tmp/lepro_hunt &>/dev/null &"
sleep 2

echo "[7] Starting tcpdump for management frames..."
$SSH "tcpdump -i wlan1mon -e -n 'type mgt' -c 500 -w /tmp/lepro_mgmt.pcap &>/dev/null &"

echo "[8] Monitoring for 30 seconds - looking for unknown MACs..."
for i in $(seq 1 6); do
    sleep 5
    echo "--- Tick $i/6 (${i}x5s) ---"
    $SSH "cat /tmp/lepro_hunt-01.csv 2>/dev/null | grep -v 'BSSID\|^$\|Station' | tail -20"
done

echo "[9] Checking PineAP client log..."
$SSH "cat /var/log/pineap.log 2>/dev/null | tail -30"

echo "[10] Checking connected clients on open AP..."
$SSH "iwinfo wlan0 assoclist 2>/dev/null"

echo "[11] Full station list from airodump..."
$SSH "cat /tmp/lepro_hunt-01.csv 2>/dev/null"

echo "=== TRAP COMPLETE ==="
