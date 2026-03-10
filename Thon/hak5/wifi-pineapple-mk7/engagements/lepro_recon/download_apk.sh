#!/bin/bash
cd /tmp
echo "Attempting APK download..."
wget -q "https://d.apkpure.net/b/APK/com.lampux.ledbrighter?version=latest" -O lampux.apk 2>&1
if [ ! -s /tmp/lampux.apk ]; then
    echo "APKPure failed, trying apkcombo..."
    wget -q "https://download.apkcombo.com/com.lampux.ledbrighter/Lepro%20LampUX_1.5.6.apk" -O lampux.apk 2>&1
fi
if [ ! -s /tmp/lampux.apk ]; then
    echo "apkcombo failed, trying direct..."
    curl -sL -o lampux.apk "https://apkpure.com/lepro-lampux/com.lampux.ledbrighter/download" 2>&1
fi
ls -la /tmp/lampux.apk 2>/dev/null || echo "DOWNLOAD FAILED"
file /tmp/lampux.apk 2>/dev/null
