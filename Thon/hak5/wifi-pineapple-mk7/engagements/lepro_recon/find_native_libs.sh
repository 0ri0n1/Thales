#!/bin/bash
cd /tmp

echo "=== Finding all native .so libraries ==="
find /tmp/lampux_extracted -name "*.so" -ls 2>/dev/null

echo ""
echo "=== Searching for key-related strings in native libs ==="
find /tmp/lampux_extracted -name "*.so" -exec strings {} \; 2>/dev/null | grep -i "A_\|encrypt\|secret\|hmac\|sign" | sort -u | head -40

echo ""
echo "=== Using jadx to decompile and search for secret construction ==="
jadx -d /tmp/lampux_jadx /tmp/lampux.apk --no-res --no-debug-info 2>&1 | tail -5

echo ""
echo "=== Searching jadx output for secret/sign construction ==="
grep -r "appEncryptSecret\|buildSecret\|signKey\|hmacKey\|doCommandNative" /tmp/lampux_jadx/sources/com/smart/ 2>/dev/null | head -20
grep -r "appEncryptSecret\|buildSecret\|signKey\|hmacKey\|doCommandNative" /tmp/lampux_jadx/sources/com/tuya/ 2>/dev/null | head -20
grep -r "appEncryptSecret\|buildSecret\|signKey\|hmacKey\|doCommandNative" /tmp/lampux_jadx/sources/com/lampux/ 2>/dev/null | head -20

echo ""
echo "DONE"
