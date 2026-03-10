#!/bin/bash
echo "=== Downloading Smart Life APK v3.6.1 (known good for key extraction) ==="
cd /tmp

wget -q "https://apkcombo.com/downloader/?package=com.tuya.smartlife&arches=arm64-v8a,armeabi-v7a&sdk=27" -O smartlife.apk 2>&1

if [ ! -s /tmp/smartlife.apk ]; then
    echo "Direct download failed, trying alternative..."
    wget -q "https://d.apkpure.net/b/APK/com.tuya.smartlife?version=latest" -O smartlife.apk 2>&1
fi

ls -la /tmp/smartlife.apk 2>/dev/null
file /tmp/smartlife.apk 2>/dev/null

echo "DONE"
