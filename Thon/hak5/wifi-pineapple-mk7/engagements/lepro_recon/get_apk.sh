#!/bin/bash
curl -sL 'https://api.github.com/repos/tuya-cloudcutter/cloudcutter-android/releases' | python3 -c "
import sys, json
releases = json.load(sys.stdin)
for r in releases[:3]:
    print(f\"Release: {r['tag_name']}\")
    for a in r.get('assets', []):
        print(f\"  {a['name']}: {a['browser_download_url']}\")
    if not r.get('assets'):
        print('  No assets')
"
