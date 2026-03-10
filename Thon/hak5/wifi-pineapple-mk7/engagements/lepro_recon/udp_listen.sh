#!/bin/bash
echo "=== Listening for Tuya UDP broadcasts on Pineapple port 6667 ==="
echo "Capturing raw hex from one broadcast packet..."

printf 'timeout 10 nc -u -l -p 6667 2>/dev/null | head -c 200 | od -A x -t x1z | head -20
' | docker exec -i kali-mcp-pentest ssh -o StrictHostKeyChecking=no root@172.16.42.1 sh 2>/dev/null

echo "DONE"
