#!/bin/bash
echo "=== Running tinytuya scan via Pineapple ==="
echo "Installing Python + tinytuya on Pineapple..."

printf 'opkg update 2>/dev/null | tail -2
opkg install python3 python3-pip 2>/dev/null | tail -5
pip3 install tinytuya 2>/dev/null | tail -3
cd /tmp
python3 -c "
import tinytuya
import json
print(\"Scanning for Tuya devices on LAN...\")
devices = tinytuya.deviceScan(verbose=False, maxretry=3)
print(\"Found\", len(devices), \"devices\")
print(json.dumps(devices, indent=2, default=str))
" 2>&1
' | docker exec -i kali-mcp-pentest ssh -o StrictHostKeyChecking=no root@172.16.42.1 sh 2>/dev/null | tail -30

echo "DONE"
