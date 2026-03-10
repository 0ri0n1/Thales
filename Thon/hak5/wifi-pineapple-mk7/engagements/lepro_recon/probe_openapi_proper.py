#!/usr/bin/env python3
"""
Proper OpenAPI probe with correct HMAC-SHA256 signing.
Tests all data center endpoints to find where the project is active.
"""
import hashlib
import hmac
import json
import requests
import time

ACCESS_ID = "dcgjmkp7tkxsxvuyt8uy"
ACCESS_SECRET = "1f238ee02ac64688986d4a8863f06eea"

ENDPOINTS = {
    "US West (AZ)":     "https://openapi.tuyaus.com",
    "US East (UEAZ)":   "https://openapi-ueaz.tuyaus.com",
    "EU Central (EU)":  "https://openapi.tuyaeu.com",
    "EU West (WEAZ)":   "https://openapi-weaz.tuyaeu.com",
    "China (CN)":       "https://openapi.tuyacn.com",
    "India (IN)":       "https://openapi.tuyain.com",
}

def get_token(base_url):
    t = str(int(time.time() * 1000))
    
    string_to_sign = ACCESS_ID + t + "GET\n" + \
        hashlib.sha256(b"").hexdigest() + "\n" + \
        "\n" + \
        "/v1.0/token?grant_type=1"
    
    sign = hmac.new(
        ACCESS_SECRET.encode(),
        string_to_sign.encode(),
        hashlib.sha256
    ).hexdigest().upper()
    
    headers = {
        "client_id": ACCESS_ID,
        "sign": sign,
        "t": t,
        "sign_method": "HMAC-SHA256",
    }
    
    resp = requests.get(f"{base_url}/v1.0/token?grant_type=1", headers=headers, timeout=10)
    return resp.json()


def get_devices(base_url, token):
    t = str(int(time.time() * 1000))
    
    string_to_sign = ACCESS_ID + token + t + "GET\n" + \
        hashlib.sha256(b"").hexdigest() + "\n" + \
        "\n" + \
        "/v1.0/iot-01/associated-user/devices"
    
    sign = hmac.new(
        ACCESS_SECRET.encode(),
        string_to_sign.encode(),
        hashlib.sha256
    ).hexdigest().upper()
    
    headers = {
        "client_id": ACCESS_ID,
        "access_token": token,
        "sign": sign,
        "t": t,
        "sign_method": "HMAC-SHA256",
    }
    
    resp = requests.get(f"{base_url}/v1.0/iot-01/associated-user/devices", headers=headers, timeout=10)
    return resp.json()


print("=" * 60)
print("TUYA OPENAPI DATA CENTER PROBE")
print("=" * 60)

for name, base in ENDPOINTS.items():
    print(f"\n--- {name} ---")
    try:
        token_resp = get_token(base)
        success = token_resp.get("success", False)
        code = token_resp.get("code", "?")
        msg = token_resp.get("msg", "?")
        print(f"  Token: success={success}, code={code}, msg={msg}")
        
        if success:
            token = token_resp["result"]["access_token"]
            uid = token_resp["result"].get("uid", "none")
            print(f"  Access Token: {token[:20]}...")
            print(f"  UID: {uid}")
            
            dev_resp = get_devices(base, token)
            print(f"  Devices: success={dev_resp.get('success')}, code={dev_resp.get('code')}")
            if dev_resp.get("success"):
                devices = dev_resp.get("result", {})
                if isinstance(devices, dict):
                    dev_list = devices.get("devices", [])
                elif isinstance(devices, list):
                    dev_list = devices
                else:
                    dev_list = []
                print(f"  Found {len(dev_list)} device(s)")
                for d in dev_list:
                    print(f"    Name: {d.get('name')}")
                    print(f"    ID: {d.get('id')}")
                    print(f"    Local Key: {d.get('local_key')}")
                    print(f"    MAC: {d.get('mac')}")
            else:
                print(f"  Devices error: {dev_resp.get('msg')}")
    except Exception as e:
        print(f"  Error: {type(e).__name__}: {e}")

print("\n\nDONE")
