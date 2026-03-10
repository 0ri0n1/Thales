#!/bin/bash
cd /tmp

echo "=== Extract APK certificate hash ==="
CERT_FILE=$(find /tmp/lampux_extracted/original/META-INF/ -name "*.RSA" -o -name "*.DSA" 2>/dev/null | head -1)
if [ -n "$CERT_FILE" ]; then
    echo "Found cert: $CERT_FILE"
    openssl pkcs7 -inform DER -print_certs -in "$CERT_FILE" -out /tmp/lampux_cert.pem 2>/dev/null
    CERT_HASH=$(openssl x509 -in /tmp/lampux_cert.pem -outform der 2>/dev/null | sha256sum | tr a-f A-F | sed 's/.\{2\}/&:/g' | cut -c 1-95)
    echo "Certificate SHA256: $CERT_HASH"
else
    echo "No RSA/DSA cert found, checking for other cert formats..."
    ls -la /tmp/lampux_extracted/original/META-INF/ 2>/dev/null
fi

echo ""
echo "=== BMP secret key extraction ==="
echo "BMP file info:"
file /tmp/lampux_extracted/assets/t_s.bmp
ls -la /tmp/lampux_extracted/assets/t_s.bmp
echo ""
echo "BMP hex header (first 128 bytes):"
xxd -l 128 /tmp/lampux_extracted/assets/t_s.bmp

echo ""
echo "=== Check for tuya-sign-hacking tools ==="
pip3 list --break-system-packages 2>/dev/null | grep -i pillow

echo ""
echo "=== Also check if the V2 image cert files exist ==="
find /tmp/lampux_extracted -path "*imageCertV2*" -ls 2>/dev/null
find /tmp/lampux_extracted -path "*smart/app/package*" -ls 2>/dev/null

echo ""
echo "=== Try building the signing secret ==="
echo "client_id: h5gw8q4artygy784ww4v"
echo "app_secret: n3s33y3j8dsy5vm4kea75p55gn3ycsdy"
echo "cert_hash: $CERT_HASH"

echo ""
echo "DONE"
