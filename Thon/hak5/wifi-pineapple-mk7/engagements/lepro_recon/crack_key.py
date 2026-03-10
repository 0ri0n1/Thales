#!/usr/bin/env python3
"""
Multi-approach Tuya local key extraction for Lampux/Lepro bulb.
Tries every available method with the credentials we have.
"""
import json
import sys
import os

EMAIL = "dallaskappel@gmail.com"
PASSWORD = "Y0urmom69!"
CLIENT_ID = "h5gw8q4artygy784ww4v"
APP_SECRET = "n3s33y3j8dsy5vm4kea75p55gn3ycsdy"
APP_SCHEMA = "lampuxledbrighter"
CERT_HASH = "37:95:F5:F7:C6:4D:79:B2:37:54:02:DD:9E:69:32:DA:38:0E:BA:8A:1E:17:94:56:25:B7:6C:7C:60:CD:63:12"

def try_tinytuya_cloud():
    """Try tinytuya Cloud with OEM app credentials directly."""
    print("\n" + "="*60)
    print("METHOD 1: tinytuya Cloud API (OEM credentials)")
    print("="*60)
    try:
        import tinytuya
        for region in ["us", "eu", "cn"]:
            print(f"\n  Trying region={region}...")
            try:
                c = tinytuya.Cloud(
                    apiRegion=region,
                    apiKey=CLIENT_ID,
                    apiSecret=APP_SECRET,
                )
                devices = c.getdevices()
                if devices and len(devices) > 0:
                    print(f"  SUCCESS! Found {len(devices)} device(s)")
                    for d in devices:
                        print(f"    Name: {d.get('name')}, Key: {d.get('key')}, ID: {d.get('id')}")
                    return devices
                else:
                    print(f"  No devices (error: {c.error})")
            except Exception as e:
                print(f"  Error: {e}")
    except ImportError:
        print("  tinytuya not installed")
    return None


def try_tuya_iot_sdk():
    """Try official Tuya IoT SDK with OEM credentials."""
    print("\n" + "="*60)
    print("METHOD 2: Official Tuya IoT Python SDK")
    print("="*60)
    try:
        from tuya_iot import TuyaOpenAPI, AuthType
        for region in ["https://openapi.tuyaus.com", "https://openapi.tuyaeu.com", "https://openapi.tuyacn.com"]:
            print(f"\n  Trying endpoint={region}...")
            try:
                api = TuyaOpenAPI(region, CLIENT_ID, APP_SECRET, AuthType.CUSTOM)
                resp = api.connect()
                print(f"  Connect response: {resp}")
                if resp.get("success"):
                    print("  Connected! Fetching devices...")
                    uid_resp = api.get(f"/v1.0/token/{api.token_info.access_token}")
                    print(f"  Token info: {uid_resp}")
                    devices_resp = api.get("/v1.0/iot-01/associated-user/devices")
                    print(f"  Devices: {devices_resp}")
                    if devices_resp.get("success"):
                        return devices_resp.get("result", {}).get("devices", [])
            except Exception as e:
                print(f"  Error: {type(e).__name__}: {e}")
    except ImportError:
        print("  tuya-iot-py-sdk not installed")
    return None


def try_tuya_iot_sdk_smart_home():
    """Try Tuya IoT SDK with Smart Home auth type."""
    print("\n" + "="*60)
    print("METHOD 3: Tuya IoT SDK - Smart Home Auth")
    print("="*60)
    try:
        from tuya_iot import TuyaOpenAPI, AuthType
        for region in ["https://openapi.tuyaus.com", "https://openapi.tuyaeu.com"]:
            print(f"\n  Trying endpoint={region}...")
            try:
                api = TuyaOpenAPI(region, CLIENT_ID, APP_SECRET)
                resp = api.connect(EMAIL, PASSWORD, "86", APP_SCHEMA)
                print(f"  Connect response: success={resp.get('success')}, code={resp.get('code')}, msg={resp.get('msg')}")
                if resp.get("success"):
                    print("  LOGGED IN! Fetching devices...")
                    uid = resp.get("result", {}).get("uid", "")
                    print(f"  UID: {uid}")
                    devices_resp = api.get(f"/v1.0/users/{uid}/devices")
                    print(f"  Devices response: {devices_resp}")
                    if devices_resp.get("success"):
                        devs = devices_resp.get("result", [])
                        for d in devs:
                            print(f"    Name: {d.get('name')}, ID: {d.get('id')}, local_key: {d.get('local_key')}")
                        return devs
            except Exception as e:
                print(f"  Error: {type(e).__name__}: {e}")
    except ImportError:
        print("  tuya-iot-py-sdk not installed")
    return None


def try_tuya_iot_sdk_country_codes():
    """Try various country codes for Smart Home auth."""
    print("\n" + "="*60)
    print("METHOD 4: Tuya IoT SDK - Multiple country codes")
    print("="*60)
    try:
        from tuya_iot import TuyaOpenAPI
        for region in ["https://openapi.tuyaus.com", "https://openapi.tuyaeu.com"]:
            for cc in ["1", "01", "91", ""]:
                print(f"\n  Trying region={region}, country_code='{cc}'...")
                try:
                    api = TuyaOpenAPI(region, CLIENT_ID, APP_SECRET)
                    resp = api.connect(EMAIL, PASSWORD, cc, APP_SCHEMA)
                    print(f"  Response: success={resp.get('success')}, code={resp.get('code')}, msg={resp.get('msg')}")
                    if resp.get("success"):
                        uid = resp.get("result", {}).get("uid", "")
                        devices_resp = api.get(f"/v1.0/users/{uid}/devices")
                        if devices_resp.get("success"):
                            devs = devices_resp.get("result", [])
                            print(f"  Found {len(devs)} device(s)!")
                            for d in devs:
                                print(f"    Name: {d.get('name')}, ID: {d.get('id')}, local_key: {d.get('local_key')}")
                            with open('/tmp/lampux_devices_final.json', 'w') as f:
                                json.dump(devs, f, indent=2)
                            print("  Saved to /tmp/lampux_devices_final.json")
                            return devs
                except Exception as e:
                    print(f"  Error: {type(e).__name__}: {e}")
    except ImportError:
        print("  tuya-iot-py-sdk not installed")
    return None


if __name__ == "__main__":
    result = try_tinytuya_cloud()
    if result:
        print("\n\n*** KEY EXTRACTED VIA METHOD 1 ***")
        sys.exit(0)

    result = try_tuya_iot_sdk()
    if result:
        print("\n\n*** KEY EXTRACTED VIA METHOD 2 ***")
        sys.exit(0)

    result = try_tuya_iot_sdk_smart_home()
    if result:
        print("\n\n*** KEY EXTRACTED VIA METHOD 3 ***")
        sys.exit(0)

    result = try_tuya_iot_sdk_country_codes()
    if result:
        print("\n\n*** KEY EXTRACTED VIA METHOD 4 ***")
        sys.exit(0)

    print("\n\nAll methods exhausted. Need Tuya IoT Platform ACCESS_ID/SECRET from Eddie.")
