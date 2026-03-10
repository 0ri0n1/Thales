#!/bin/bash
echo "=== LAMPUX APK DECOMPILE ==="

cd /tmp

# Download from multiple sources
echo "[1] Downloading APK..."
pip install gplaydl 2>/dev/null || true

# Try apkcombo
wget -q --timeout=15 "https://download.apkcombo.com/com.lampux.ledbrighter/Lepro%20LampUX_1.8.2_apkcombo.com.apk" -O lampux.apk 2>/dev/null

if [ ! -s lampux.apk ]; then
    # Try apkpure mirror
    wget -q --timeout=15 "https://d.apkpure.com/b/APK/com.lampux.ledbrighter?version=latest" -O lampux.apk 2>/dev/null
fi

if [ ! -s lampux.apk ]; then
    echo "Direct download failed. Trying apkeep..."
    pip3 install apkeep 2>/dev/null
    apkeep -a com.lampux.ledbrighter . 2>/dev/null
    ls -la com.lampux.ledbrighter*.apk 2>/dev/null && mv com.lampux.ledbrighter*.apk lampux.apk 2>/dev/null
fi

if [ ! -s lampux.apk ]; then
    echo "All download methods failed."
    echo "Trying jadx on cached APKs or known credentials approach instead."
    
    # Use apktool to search PlayStore cache or local copies
    echo ""
    echo "ALTERNATIVE: Trying to find Lampux keys from Tuya OEM app database..."
    echo "Checking tuya-sign-hacking known keys..."
    
    # The Lampux app page at smartapp.tuya.com reveals the internal name: lampuxledbrighter
    # Try using the known format to construct the credentials
    echo ""
    echo "App package: com.lampux.ledbrighter"
    echo "Tuya smart app ID: lampuxledbrighter"
    echo ""
    echo "Without the APK, cannot extract client_id and secret."
    echo "Recommend: User adds device to Smart Life app (free, same Tuya cloud)"
    exit 1
fi

echo "[2] APK downloaded: $(ls -la lampux.apk | awk '{print $5}') bytes"

# Decompile with jadx if available
if which jadx >/dev/null 2>&1; then
    echo "[3] Decompiling with jadx..."
    jadx lampux.apk -d lampux_src --no-res --no-debug-info 2>/dev/null
    
    echo "[4] Searching for Tuya credentials..."
    echo "--- clientId/appSecret ---"
    grep -rn "initKey\|clientId\|appSecret\|3fjrekux\|ekmnwp9f" lampux_src/ 2>/dev/null | head -20
    grep -rn "const-string.*[a-z0-9]\{20\}" lampux_src/ 2>/dev/null | grep -i "key\|secret\|client" | head -20
    
    echo "--- BMP file location ---"
    find lampux_src/ -name "*.bmp" 2>/dev/null
    grep -rn "\.bmp\|t_s\.bmp\|dF9z" lampux_src/ 2>/dev/null | head -10
    
    echo "--- API endpoints ---"
    grep -rn "tuya\.com\|mb-gw\|a1\.tuya" lampux_src/ 2>/dev/null | head -10
else
    echo "[3] jadx not found, trying apktool..."
    apktool d lampux.apk -o lampux_dec -f 2>/dev/null
    
    echo "[4] Searching smali for credentials..."
    grep -rn "const-string.*[a-z0-9]\{20,\}" lampux_dec/smali*/ 2>/dev/null | grep -i "key\|secret\|client\|init" | head -30
    
    echo "--- BMP ---"
    find lampux_dec/assets/ -name "*.bmp" 2>/dev/null
fi

echo "=== DONE ==="
