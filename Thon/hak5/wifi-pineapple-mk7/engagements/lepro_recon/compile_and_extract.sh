#!/bin/bash
cd /tmp/tuya-sign-hacking/read-keys-from-bmp

echo "=== Compiling BMP extraction tools ==="
cat compile.sh
bash compile.sh 2>&1

echo ""
echo "=== Testing with known good BMP first ==="
ls -la extract_used_pixels read_keys 2>/dev/null

echo ""
echo "=== Extracting Lampux BMP key ==="
./extract_used_pixels h5gw8q4artygy784ww4v /tmp/lampux_extracted/assets/t_s.bmp /tmp/lampux_pixels.bmp 2>&1
echo ""
./read_keys h5gw8q4artygy784ww4v /tmp/lampux_pixels.bmp 2>&1

echo ""
echo "=== Constructing full signing secret ==="
echo "Format: certHash_bmpKey_appSecret"
echo "Or simplified: A_bmpKey_appSecret"
echo ""
echo "DONE"
