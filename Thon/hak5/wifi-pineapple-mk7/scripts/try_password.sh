#!/bin/bash
# Try common Pineapple passwords
for pass in "" "hak5pineapple" "pineapple" "hak5" "root" "toor"; do
    echo "Trying password: '$pass'"
    sshpass -p "$pass" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@172.16.42.1 'echo AUTH_OK; uptime' 2>&1
    rc=$?
    if [ $rc -eq 0 ]; then
        echo "SUCCESS with password: '$pass'"
        break
    fi
    echo "Failed (rc=$rc)"
    echo ""
done
