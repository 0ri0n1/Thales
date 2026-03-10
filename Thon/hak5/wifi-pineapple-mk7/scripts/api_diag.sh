#!/bin/bash
# Pineapple MK7 API diagnostic
# The MK7 API requires authentication - try to get status via API
HOST="http://172.16.42.1:1471"

echo "=== Checking API endpoints ==="

echo ""
echo "--- /api/status ---"
curl -s --connect-timeout 5 "$HOST/api/status" 2>&1
echo ""

echo ""
echo "--- /api/pineap/status ---"
curl -s --connect-timeout 5 "$HOST/api/pineap/status" 2>&1
echo ""

echo ""
echo "--- /api/pineap/clients ---"
curl -s --connect-timeout 5 "$HOST/api/pineap/clients" 2>&1
echo ""

echo ""
echo "--- /api/pineap/ssids ---"
curl -s --connect-timeout 5 "$HOST/api/pineap/ssids" 2>&1
echo ""

echo ""
echo "--- /api/recon/scans ---"
curl -s --connect-timeout 5 "$HOST/api/recon/scans" 2>&1
echo ""

echo ""
echo "--- /api/notifications ---"
curl -s --connect-timeout 5 "$HOST/api/notifications" 2>&1
echo ""

echo ""
echo "--- Try unauthenticated command exec ---"
curl -s --connect-timeout 5 -X POST "$HOST/api/cmd" \
  -H "Content-Type: application/json" \
  -d '{"cmd":"iwconfig 2>&1"}' 2>&1
echo ""

echo ""
echo "--- /api/dashboard ---"
curl -s --connect-timeout 5 "$HOST/api/dashboard" 2>&1
echo ""

echo "=== API DIAG DONE ==="
