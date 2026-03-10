#!/bin/bash
printf '#!/bin/sh\nssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 root@172.16.42.1 "nohup tcpdump -i wlan2 -w /tmp/lepro_capture.pcap host 192.168.1.82 >/dev/null 2>/dev/null" </dev/null\n' | docker exec -i kali-mcp-pentest tee /tmp/start_capture.sh

docker exec kali-mcp-pentest chmod +x /tmp/start_capture.sh
echo "Script deployed. Starting capture..."
docker exec kali-mcp-pentest bash /tmp/start_capture.sh
echo "Capture command sent. Verifying..."
sleep 3
printf 'ps | grep tcpdump | grep -v grep\n' | docker exec -i kali-mcp-pentest ssh -o StrictHostKeyChecking=no root@172.16.42.1 sh 2>/dev/null
echo "Done."
