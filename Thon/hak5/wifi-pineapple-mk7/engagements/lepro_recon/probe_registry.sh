#!/bin/bash
echo "=== Fetching Tuya App Registry for Lampux ==="
curl -s "https://smartapp.tuya.com/lampuxledbrighter" | python3 -c "
import sys, json, re
html = sys.stdin.read()

# Look for JSON data embedded in the page
json_matches = re.findall(r'(\{[^{}]{50,}\})', html)
for m in json_matches:
    try:
        d = json.loads(m)
        print(json.dumps(d, indent=2))
    except:
        pass

# Look for script tags with data
script_matches = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
for s in script_matches:
    if 'lampux' in s.lower() or 'clientId' in s or 'schema' in s:
        print('SCRIPT:', s[:500])
        
# Look for any key-value pairs
kv_matches = re.findall(r'\"(\w+)\":\s*\"([^\"]+)\"', html)
for k, v in kv_matches:
    if any(x in k.lower() for x in ['key', 'id', 'schema', 'region', 'secret', 'client', 'data_center', 'server', 'api']):
        print(f'  {k}: {v}')
" 2>&1

echo ""
echo "=== Raw HTML inspection ==="
curl -s "https://smartapp.tuya.com/lampuxledbrighter" | grep -i "region\|datacenter\|data_center\|server\|endpoint\|api_url\|china\|schema" | head -20

echo ""
echo "DONE"
