#!/bin/bash
cd /tmp/tuya-sign-hacking/read-keys-from-bmp

echo "=== Trying fixed_key.bmp with production client_id ==="
./extract_used_pixels h5gw8q4artygy784ww4v /tmp/lampux_extracted/assets/fixed_key.bmp /tmp/fixed_pixels.bmp 2>&1
./read_keys h5gw8q4artygy784ww4v /tmp/fixed_pixels.bmp 2>&1

echo ""
echo "=== Trying fixed_key.bmp with debug client_id ==="
./extract_used_pixels fynxsujx8yavn5p7rcmr /tmp/lampux_extracted/assets/fixed_key.bmp /tmp/fixed_pixels_dbg.bmp 2>&1
./read_keys fynxsujx8yavn5p7rcmr /tmp/fixed_pixels_dbg.bmp 2>&1

echo ""
echo "=== Trying t_s.bmp with debug client_id ==="
./extract_used_pixels fynxsujx8yavn5p7rcmr /tmp/lampux_extracted/assets/t_s.bmp /tmp/ts_pixels_dbg.bmp 2>&1
./read_keys fynxsujx8yavn5p7rcmr /tmp/ts_pixels_dbg.bmp 2>&1

echo ""
echo "=== Compare the two BMP files ==="
md5sum /tmp/lampux_extracted/assets/fixed_key.bmp /tmp/lampux_extracted/assets/t_s.bmp

echo ""
echo "=== Testing with test BMP from tuya-sign-hacking repo ==="
echo "The repo has a known-good test.bmp. If our tool works at all:"
./extract_used_pixels 3fjrekuxank9eaej3gcx /tmp/tuya-sign-hacking/read-keys-from-bmp/test.bmp /tmp/test_pixels.bmp 2>&1
./read_keys 3fjrekuxank9eaej3gcx /tmp/test_pixels.bmp 2>&1

echo ""
echo "DONE"
