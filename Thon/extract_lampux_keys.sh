#!/bin/bash
# Extract Tuya API credentials from Lampux APK using Kali tools

echo "=== LAMPUX APK CREDENTIAL EXTRACTION ==="

# Download Lampux APK from APKPure/Aptoide
echo "[1] Downloading Lampux APK..."
cd /tmp
wget -q "https://d.apkpure.net/b/APK/com.lampux.ledbrighter?version=latest" -O lampux.apk 2>/dev/null || \
  wget -q "https://pool.apk.aptoide.com/lampux/com-lampux-ledbrighter-138-71310138-d1d56b40beedc39e3e6ad05b5e119fa3.apk" -O lampux.apk 2>/dev/null || \
  echo "Direct download failed, trying pip approach"

if [ ! -f lampux.apk ] || [ ! -s lampux.apk ]; then
    echo "APK download failed. Trying alternative: use tuya-sign-hacking bmp reader directly"
    echo "Falling back to known Tuya/SmartLife credentials as proxy..."
    
    # Use known SmartLife credentials (many Lepro/Lampux devices work with SmartLife too)
    echo ""
    echo "=== KNOWN TUYA OEM CREDENTIALS ==="
    echo "TuyaSmart:"
    echo "  clientId: 3fjrekuxank9eaej3gcx"
    echo "  secret:   aq7xvqcyqcnegvew793pqjmhv77rneqc"
    echo ""
    echo "SmartLife:"
    echo "  clientId: ekmnwp9f5pnh3trdtpgy"  
    echo "  secret:   r3me7ghmxjevrvnpemwmhw3fxtacphyg"
    echo ""
    echo "Try linking Lampux device to Smart Life app instead for key extraction"
    exit 0
fi

echo "[2] Decompiling APK..."
which apktool >/dev/null 2>&1 && apktool d lampux.apk -o lampux_decoded -f 2>/dev/null
which jadx >/dev/null 2>&1 && jadx lampux.apk -d lampux_jadx --no-res 2>/dev/null

echo "[3] Searching for clientId/appSecret..."
grep -rn "clientId\|appSecret\|appKey\|secret" lampux_decoded/smali/ 2>/dev/null | grep "const-string" | head -20
grep -rn "clientId\|appSecret\|appKey\|secret" lampux_jadx/ 2>/dev/null | grep -v ".class" | head -20

echo "[4] Searching for BMP steganography file..."
find lampux_decoded/assets/ -name "*.bmp" 2>/dev/null
find lampux_decoded/ -name "t_s.bmp" 2>/dev/null

echo "[5] Certificate hash..."
if [ -d lampux_decoded/original/META-INF ]; then
    for cert in lampux_decoded/original/META-INF/*.RSA lampux_decoded/original/META-INF/*.DSA; do
        if [ -f "$cert" ]; then
            openssl pkcs7 -inform DER -print_certs -in "$cert" -out /tmp/lampux_cert.pem 2>/dev/null
            HASH=$(openssl x509 -in /tmp/lampux_cert.pem -outform der 2>/dev/null | sha256sum | tr a-f A-F | sed 's/.\{2\}/&:/g' | cut -c 1-95)
            echo "  certSign: $HASH"
        fi
    done
fi

echo "=== DONE ==="
