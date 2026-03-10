#!/bin/bash

echo "=== Search for imageCertV2 references ==="
grep -r "imageCertV2" /tmp/lampux_jadx/sources/ 2>/dev/null | head -20

echo ""
echo "=== Search for HMAC signing code ==="
grep -rn "HmacSHA256\|SecretKeySpec\|hmac" /tmp/lampux_jadx/sources/com/thingclips/ 2>/dev/null | head -20
grep -rn "HmacSHA256\|SecretKeySpec\|hmac" /tmp/lampux_jadx/sources/com/tuya/ 2>/dev/null | head -20

echo ""
echo "=== ThingNGConfig full content ==="
cat /tmp/lampux_jadx/sources/com/smart/app/ThingNGConfig.java 2>/dev/null

echo ""
echo "=== Search for sign/secret construction in thingclips SDK ==="
grep -rn "buildSignKey\|signKey\|getSecret\|getSignKey" /tmp/lampux_jadx/sources/ 2>/dev/null | head -30

echo ""
echo "DONE"
