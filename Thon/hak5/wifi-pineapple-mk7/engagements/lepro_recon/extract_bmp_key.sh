#!/bin/bash
cd /tmp

echo "=== Cloning tuya-sign-hacking ==="
git clone https://github.com/nalajcie/tuya-sign-hacking.git 2>&1 | tail -3

echo ""
echo "=== Installing Pillow for BMP processing ==="
pip3 install --break-system-packages Pillow 2>&1 | tail -3

echo ""
echo "=== Running BMP key extraction ==="
cd /tmp/tuya-sign-hacking
ls -la *.py 2>/dev/null
python3 extract_used_pixels.py h5gw8q4artygy784ww4v /tmp/lampux_extracted/assets/t_s.bmp /tmp/lampux_used_pixels.bmp 2>&1
echo ""
python3 read_keys.py h5gw8q4artygy784ww4v /tmp/lampux_used_pixels.bmp 2>&1

echo ""
echo "DONE"
