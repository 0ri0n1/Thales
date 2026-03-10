#!/bin/bash
echo "Starting phone-to-bulb capture on Pineapple..."
printf 'nohup tcpdump -i wlan2 -w /tmp/phone_bulb.pcap "host 192.168.1.78 and host 192.168.1.82" >/dev/null 2>/dev/null &\nsleep 1\nps | grep tcpdump | grep -v grep\n' | docker exec -i kali-mcp-pentest ssh -o StrictHostKeyChecking=no root@172.16.42.1 sh 2>/dev/null
echo "Done starting capture."
