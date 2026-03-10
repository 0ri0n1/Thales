#!/usr/bin/env python3
import sys
sys.path.insert(0, '/tmp/tuya-uncover')
from uncover import TuyaCloudApiOEM, InvalidAuthentication

EMAIL = "dallaskappel@gmail.com"
PASSWORD = "Y0urmom69!"
CLIENT_ID = "h5gw8q4artygy784ww4v"
APP_SECRET = "n3s33y3j8dsy5vm4kea75p55gn3ycsdy"
CERT_HASH = "37:95:F5:F7:C6:4D:79:B2:37:54:02:DD:9E:69:32:DA:38:0E:BA:8A:1E:17:94:56:25:B7:6C:7C:60:CD:63:12"

secret_patterns = [
    ("A prefix (simplified)", f"A_{APP_SECRET}_{APP_SECRET}"),
    ("A_secret only", f"A_{APP_SECRET}"),
    ("cert_secret_secret", f"{CERT_HASH}_{APP_SECRET}_{APP_SECRET}"),
    ("raw secret", APP_SECRET),
]

regions = ["us", "eu"]

for region in regions:
    for name, secret in secret_patterns:
        print(f"\n--- Trying region={region}, pattern='{name}' ---")
        print(f"    secret length: {len(secret)}")
        try:
            api = TuyaCloudApiOEM(
                cloud_type="oem_generic",
                region=region,
                username=EMAIL,
                password=PASSWORD,
                client_id=CLIENT_ID,
                secret=secret,
            )
            api.login()
            print(f"  LOGIN SUCCESS! SID: {api._sid}")
            
            print("  Fetching devices...")
            devs = api.list_devices(map_tt_compat=True, include_raw=True)
            print(f"  Found {len(devs)} devices:")
            import json
            print(json.dumps(devs, indent=2, default=str))
            
            with open('/tmp/lampux_devices.json', 'w') as f:
                json.dump(devs, f, indent=2, default=str)
            print("\n  Saved to /tmp/lampux_devices.json")
            sys.exit(0)
            
        except InvalidAuthentication as e:
            print(f"  Auth failed: {e}")
        except Exception as e:
            print(f"  Error: {type(e).__name__}: {e}")

print("\n\nAll patterns failed. Need to extract the BMP key for the correct signing secret.")
