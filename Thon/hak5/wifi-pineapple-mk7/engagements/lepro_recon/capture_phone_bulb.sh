#!/bin/bash

echo "=== Starting capture of phone-to-bulb LAN traffic ==="
echo "Phone: 192.168.1.78, Bulb: 192.168.1.82"
echo "Looking for Tuya LAN control on ports 6666-6668"

printf 'nohup tcpdump -i wlan2 -w /tmp/phone_bulb_capture.pcap "host 192.168.1.78 and host 192.168.1.82" >/dev/null 2>/dev/null &\n' | docker exec -i kali-mcp-pentest ssh -o StrictHostKeyChecking=no root@172.16.42.1 sh 2>/dev/null

sleep 2

printf 'ps | grep tcpdump | grep -v grep\n' | docker exec -i kali-mcp-pentest ssh -o StrictHostKeyChecking=no root@172.16.42.1 sh 2>/dev/null

echo ""
echo "Capture running. Eddie needs to open the Lampux app and toggle the bulb."
echo "Will capture for 60 seconds..."
sleep 60

printf 'kill $(ps | grep tcpdump | grep -v grep | awk "{print \$1}") 2>/dev/null\nsleep 1\nls -la /tmp/phone_bulb_capture.pcap\ntcpdump -r /tmp/phone_bulb_capture.pcap 2>/dev/null | wc -l\n' | docker exec -i kali-mcp-pentest ssh -o StrictHostKeyChecking=no root@172.16.42.1 sh 2>/dev/null

echo ""
echo "=== Transfer capture ==="
docker exec kali-mcp-pentest scp -o StrictHostKeyChecking=no root@172.16.42.1:/tmp/phone_bulb_capture.pcap /tmp/phone_bulb_capture.pcap 2>/dev/null

echo ""
echo "=== Quick analysis ==="
echo 'tshark -r /tmp/phone_bulb_capture.pcap -q -z conv,ip 2>/dev/null' | docker exec -i kali-mcp-pentest bash
echo 'tshark -r /tmp/phone_bulb_capture.pcap -q -z io,phs 2>/dev/null' | docker exec -i kali-mcp-pentest bash

echo ""
echo "DONE"
