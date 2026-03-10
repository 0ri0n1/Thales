#!/bin/bash
echo "=== .so files in APK ==="
unzip -l /tmp/lampux.apk | grep "\.so$" | head -40
echo ""
echo "=== Specifically libc++ ==="
unzip -l /tmp/lampux.apk | grep "libc++"
echo ""
echo "=== ARM64 libs ==="
unzip -l /tmp/lampux.apk | grep "arm64"
echo ""
echo "DONE"
