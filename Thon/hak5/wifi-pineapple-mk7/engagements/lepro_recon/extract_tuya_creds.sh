#!/bin/bash
cd /tmp
echo "=== Step 1: Extracting APK with apktool ==="
apktool d -f -o /tmp/lampux_extracted lampux.apk 2>&1 | tail -5

echo ""
echo "=== Step 2: Searching for Tuya client_id / secret in strings.xml ==="
grep -ri "appEncryptKey\|appEncryptSecret\|clientId\|client_id\|tuya.*key\|tuya.*secret" /tmp/lampux_extracted/res/values/strings.xml 2>/dev/null | head -20

echo ""
echo "=== Step 3: Searching for clientId in smali code ==="
grep -r "clientId\|client_id\|appkey\|appsecret\|appEncrypt" /tmp/lampux_extracted/smali*/com/smart/ 2>/dev/null | head -20
grep -r "clientId\|client_id\|appkey\|appsecret\|appEncrypt" /tmp/lampux_extracted/smali*/com/lampux/ 2>/dev/null | head -20

echo ""
echo "=== Step 4: Searching for t_s.bmp (BMP secret key) ==="
find /tmp/lampux_extracted -name "t_s.bmp" -ls 2>/dev/null

echo ""
echo "=== Step 5: Broad search for 20-char hex strings that look like client_ids ==="
grep -rhoP '[a-z0-9]{20}' /tmp/lampux_extracted/res/values/strings.xml 2>/dev/null | sort -u | head -20

echo ""
echo "=== Step 6: Check AndroidManifest for Tuya references ==="
grep -i "tuya" /tmp/lampux_extracted/AndroidManifest.xml 2>/dev/null | head -10

echo ""
echo "=== Step 7: Full strings.xml dump for manual inspection ==="
cat /tmp/lampux_extracted/res/values/strings.xml 2>/dev/null | grep -i "key\|secret\|encrypt\|tuya\|client\|app_id\|appid" | head -30

echo ""
echo "DONE"
