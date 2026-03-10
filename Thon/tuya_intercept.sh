#!/bin/bash
export SSHPASS=Mousepad7
SSH="sshpass -e ssh -o StrictHostKeyChecking=no root@172.16.42.1"
echo "Capturing Tuya bulb traffic from Pineapple wlan2..."
$SSH "timeout 30 tcpdump -i wlan2 -nn host 192.168.1.82 -c 100 -w /tmp/tuya_capture.pcap 2>/dev/null" &
sleep 32
$SSH "tcpdump -r /tmp/tuya_capture.pcap -nn 2>/dev/null | head -50"