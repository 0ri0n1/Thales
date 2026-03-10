#!/usr/bin/env python3
"""
Query all possible device listing endpoints with proper auth.
"""
import hashlib
import hmac
import json
import requests
import time

ACCESS_ID = "dcgjmkp7tkxsxvuyt8uy"
ACCESS_SECRET = "1f238ee02ac64688986d4a8863f06eea"
BASE = "https://openapi.tuyaus.com"

def sign_request(method, path, token="", body=b""):
    t = str(int(time.time() * 1000))
    content_hash = hashlib.sha256(body).hexdigest()
    string_to_sign = ACCESS_ID + token + t + method + "\n" + content_hash + "\n\n" + path
    sign = hmac.new(
        ACCESS_SECRET.encode(), string_to_sign.encode(), hashlib.sha256
    ).hexdigest().upper()
    headers = {
        "client_id": ACCESS_ID,
        "sign": sign,
        "t": t,
        "sign_method": "HMAC-SHA256",
    }
    if token:
        headers["access_token"] = token
    return headers

# Get token
headers = sign_request("GET", "/v1.0/token?grant_type=1")
resp = requests.get(f"{BASE}/v1.0/token?grant_type=1", headers=headers, timeout=10)
token_data = resp.json()
TOKEN = token_data["result"]["access_token"]
print(f"Token: {TOKEN[:20]}...")
print(f"UID: {token_data['result'].get('uid')}")

# Try multiple device listing endpoints
paths = [
    "/v1.0/devices",
    "/v1.1/devices",
    "/v1.0/users/bay1773112196399wp60/devices",
    "/v2.0/cloud/thing/device",
    "/v1.0/iot-03/devices",
    "/v1.3/iot-03/devices",
    "/v1.0/cloud/thing/device",
    "/v1.0/devices?page_no=1&page_size=20",
    "/v1.2/cloud/thing/device",
]

print("\n=== Trying device listing endpoints ===\n")
for path in paths:
    clean_path = path.split("?")[0] if "?" in path else path
    headers = sign_request("GET", path, token=TOKEN)
    try:
        resp = requests.get(f"{BASE}{path}", headers=headers, timeout=10)
        result = resp.json()
        success = result.get("success", False)
        code = result.get("code", "?")
        msg = result.get("msg", "?")
        print(f"  {path}")
        print(f"    success={success}, code={code}, msg={msg}")
        if success and result.get("result"):
            print(f"    RESULT: {json.dumps(result['result'], indent=4)[:500]}")
    except Exception as e:
        print(f"  {path}: {type(e).__name__}: {e}")

# Try to list linked app accounts
print("\n=== Checking linked app accounts ===\n")
acct_paths = [
    "/v1.0/token/bay1773112196399wp60",
    "/v1.0/apps/token",
]
for path in acct_paths:
    headers = sign_request("GET", path, token=TOKEN)
    try:
        resp = requests.get(f"{BASE}{path}", headers=headers, timeout=10)
        result = resp.json()
        print(f"  {path}: success={result.get('success')}, code={result.get('code')}, msg={result.get('msg')}")
        if result.get("success") and result.get("result"):
            print(f"    {json.dumps(result['result'], indent=2)[:500]}")
    except Exception as e:
        print(f"  {path}: {e}")

# Now try with tinytuya Cloud which handles signing properly
print("\n=== Using tinytuya Cloud (handles signing) ===\n")
import tinytuya
for region in ["us", "eu"]:
    c = tinytuya.Cloud(apiRegion=region, apiKey=ACCESS_ID, apiSecret=ACCESS_SECRET)
    devices = c.getdevices()
    print(f"  Region {region}: {len(devices) if devices else 0} devices, error={c.error}")
    if devices:
        for d in devices:
            print(f"    {d.get('name')}: key={d.get('key')}, id={d.get('id')}")

print("\nDONE")
