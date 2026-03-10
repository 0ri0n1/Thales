#!/bin/bash
echo "=== Trying to fetch V2 BMP image from Tuya CDN ==="

BMP_PATH="smart/app/package/10420/imageCertV2_1693375651852_760.bmp"

URLS=(
    "https://images.tuyaus.com/${BMP_PATH}"
    "https://images.tuyaeu.com/${BMP_PATH}"
    "https://images.tuyacn.com/${BMP_PATH}"
    "https://airtake-public-data-1254153901.cos.ap-shanghai.myqcloud.com/${BMP_PATH}"
    "https://airtake-public-data.oss-cn-hangzhou.aliyuncs.com/${BMP_PATH}"
    "https://images.tuyaus.com/smart/app/package/10420/imageCertV2_1693375651852_760.bmp"
)

for url in "${URLS[@]}"; do
    echo ""
    echo "Trying: $url"
    HTTP_CODE=$(curl -s -o /tmp/v2_cert.bmp -w "%{http_code}" "$url" 2>/dev/null)
    echo "  HTTP Status: $HTTP_CODE"
    if [ "$HTTP_CODE" = "200" ]; then
        FILE_SIZE=$(stat -c%s /tmp/v2_cert.bmp 2>/dev/null)
        echo "  File size: $FILE_SIZE bytes"
        file /tmp/v2_cert.bmp 2>/dev/null
        if [ "$FILE_SIZE" -gt 100 ]; then
            echo "  SUCCESS! Downloaded V2 BMP cert"
            echo ""
            echo "=== Now trying to extract the key ==="
            cd /tmp/tuya-sign-hacking/read-keys-from-bmp
            ./extract_used_pixels h5gw8q4artygy784ww4v /tmp/v2_cert.bmp /tmp/v2_pixels.bmp 2>&1
            ./read_keys h5gw8q4artygy784ww4v /tmp/v2_pixels.bmp 2>&1
            exit 0
        fi
    fi
done

echo ""
echo "=== Could not fetch V2 BMP from CDN ==="
echo "Trying alternate approach: check if BMP is embedded in APK assets..."
find /tmp/lampux_extracted/assets -name "*.bmp" -ls 2>/dev/null
find /tmp/lampux_extracted/res -name "*.bmp" -ls 2>/dev/null

echo ""
echo "=== Checking if imageCertV2 files exist in extracted APK ==="
find /tmp/lampux_extracted -name "*imageCert*" -ls 2>/dev/null
find /tmp/lampux_extracted -name "*certV2*" -ls 2>/dev/null

echo ""
echo "DONE"
