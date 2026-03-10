#!/bin/bash
cd /tmp

echo "=== Analyzing known vendor secret formats ==="
python3 -c "
import json
secrets = {
    'smartlife': '0F:C3:61:99:9C:C0:C3:5B:A8:AC:A5:7D:AA:55:93:A2:0C:F5:57:27:70:2E:A8:5A:D7:B3:22:89:49:F8:88:FE_jfg5rs5kkmrj5mxahugvucrsvw43t48x_r3me7ghmxjevrvnpemwmhw3fxtacphyg',
    'tuya': '93:21:9F:C2:73:E2:20:0F:4A:DE:E5:F7:19:1D:C6:56:BA:2A:2D:7B:2F:F5:D2:4C:D5:5C:4B:61:55:00:1E:40_aq7xvqcyqcnegvew793pqjmhv77rneqc_vay9g59g9g99qf3rtqptmc3emhkanwkx',
    'gosund': 'A_pqdyxyx3uhk337sxxumdgfry3awaxysm_wm8hvxahqhcvvnpqgurympm4ppfgxxnm',
    'birdlover': 'A_x4y4ds9nysv4d3agjyqwmvnptwhgtcwu_pku4cchspfmskfgtaacqcvkfdscx7u7t',
    'sylvania': 'A_ag4xcmp9rjttkj9yf9e8c3wfxry7yr44_wparh3scdv8dc7rrnuegaf9mqmn4snpk',
}

print('Vendor | Parts | Cert | BMP Key Len | Secret Len')
print('-' * 70)
for vendor, secret in secrets.items():
    parts = secret.split('_')
    cert = parts[0]
    bmp_key = parts[1] if len(parts) > 1 else 'N/A'
    app_secret = parts[2] if len(parts) > 2 else 'N/A'
    print(f'{vendor:15s} | {len(parts)} | {cert[:6]:6s}... | {len(bmp_key):3d} | {len(app_secret):3d}')
    
print()
print('Pattern: certHash_bmpKey_appSecret')
print('Where certHash is either full SHA256 hash or just \"A\"')
print('BMP key is 32 chars, app_secret is 32 chars')
print()
print('Our Lampux values:')
print(f'  client_id: h5gw8q4artygy784ww4v (len={len(\"h5gw8q4artygy784ww4v\")})')
print(f'  app_secret: n3s33y3j8dsy5vm4kea75p55gn3ycsdy (len={len(\"n3s33y3j8dsy5vm4kea75p55gn3ycsdy\")})')
print(f'  cert_hash: 37:95:F5:F7:C6:4D:79:B2:37:54:02:DD:9E:69:32:DA:38:0E:BA:8A:1E:17:94:56:25:B7:6C:7C:60:CD:63:12')
print()
print('We need the BMP key. But many OEM apps use simplified A_ prefix.')
print('Trying both patterns...')
print()
print('Test secret 1 (simplified): A_???_n3s33y3j8dsy5vm4kea75p55gn3ycsdy')
print('  -> We need the BMP key which is 32 chars')
print()
print('Test secret 2 (full cert): 37:95:F5:F7:C6:4D:79:B2:37:54:02:DD:9E:69:32:DA:38:0E:BA:8A:1E:17:94:56:25:B7:6C:7C:60:CD:63:12_???_n3s33y3j8dsy5vm4kea75p55gn3ycsdy')
"

echo ""
echo "=== Searching for BMP V2 extraction tools ==="
cd /tmp/tuya-sign-hacking
grep -ri "V2\|v2\|imageCert" README.md 2>/dev/null | head -10

echo ""
echo "=== Checking if the app has a libjnimain.so we can use ==="
find /tmp/lampux_extracted -name "libjnimain.so" -ls 2>/dev/null
find /tmp/lampux_extracted -name "*jni*main*" -ls 2>/dev/null

echo ""
echo "DONE"
