#!/usr/bin/env python3
"""
Probe the Lampux/Tuya OEM API endpoints to understand account structure.
READ-ONLY reconnaissance — no exploitation.
"""
import hashlib
import json
import requests
import time

EMAIL = "dallaskappel@gmail.com"
CLIENT_ID = "h5gw8q4artygy784ww4v"

REGIONS = {
    "us": "https://a1.tuyaus.com/api.json",
    "eu": "https://a1.tuyaeu.com/api.json",
    "cn": "https://a1.tuyacn.com/api.json",
    "in": "https://a1.tuyain.com/api.json",
}

def probe_region(name, endpoint):
    """Check if this region recognizes the Lampux account."""
    print(f"\n--- Probing {name}: {endpoint} ---")
    
    params = {
        "a": "tuya.m.user.email.token.create",
        "clientId": CLIENT_ID,
        "v": "1.0",
        "time": str(int(time.time())),
    }
    
    payload = {
        "countryCode": "",
        "email": EMAIL,
    }
    
    data = {"postData": json.dumps(payload, separators=(",", ":"))}
    
    # Send unsigned request to see what error we get
    # This tells us if the region/client_id combo is valid
    try:
        resp = requests.post(endpoint, params=params, data=data, timeout=10)
        result = resp.json()
        print(f"  Status: {resp.status_code}")
        print(f"  Success: {result.get('success')}")
        print(f"  Error Code: {result.get('errorCode', 'none')}")
        print(f"  Error Msg: {result.get('errorMsg', 'none')}")
        print(f"  Full response: {json.dumps(result, indent=2)}")
        return result
    except Exception as e:
        print(f"  Error: {type(e).__name__}: {e}")
        return None


def probe_app_info():
    """Query Tuya's public app registry for Lampux info."""
    print("\n=== Probing Tuya App Registry ===")
    urls = [
        "https://smartapp.tuya.com/lampuxledbrighter",
        "https://h5.tuyaus.com/lampuxledbrighter",
    ]
    for url in urls:
        try:
            resp = requests.get(url, timeout=10)
            print(f"  {url}: HTTP {resp.status_code}, length={len(resp.text)}")
        except Exception as e:
            print(f"  {url}: {type(e).__name__}: {e}")


def probe_openapi_endpoints():
    """Check which Tuya OpenAPI endpoints respond to our IoT Platform creds."""
    print("\n=== Probing Tuya OpenAPI with IoT Platform creds ===")
    
    ACCESS_ID = "dcgjmkp7tkxsxvuyt8uy"
    ACCESS_SECRET = "1f238ee02ac64688986d4a8863f06eea"
    
    endpoints = {
        "US West": "https://openapi.tuyaus.com",
        "EU Central": "https://openapi.tuyaeu.com", 
        "China": "https://openapi.tuyacn.com",
        "India": "https://openapi.tuyain.com",
        "US East": "https://openapi-ueaz.tuyaus.com",
        "EU West": "https://openapi-weaz.tuyaeu.com",
    }
    
    for name, base in endpoints.items():
        try:
            t = str(int(time.time() * 1000))
            sign_str = ACCESS_ID + t
            sign = hashlib.sha256(
                (sign_str + ACCESS_SECRET).encode()
            ).hexdigest().upper()
            
            # Simplified — just checking connectivity
            headers = {
                "client_id": ACCESS_ID,
                "sign": sign,
                "t": t,
                "sign_method": "HMAC-SHA256",
            }
            resp = requests.get(f"{base}/v1.0/token?grant_type=1", headers=headers, timeout=10)
            result = resp.json()
            success = result.get("success", False)
            code = result.get("code", "?")
            msg = result.get("msg", "?")
            print(f"  {name:15s} ({base}): success={success}, code={code}, msg={msg}")
        except Exception as e:
            print(f"  {name:15s}: {type(e).__name__}: {e}")


def probe_user_exists():
    """Check if user exists on each region using minimal API call."""
    print("\n=== Checking user existence per region ===")
    
    for name, endpoint in REGIONS.items():
        params = {
            "a": "tuya.m.user.email.check",
            "clientId": CLIENT_ID,
            "v": "1.0",
            "time": str(int(time.time())),
        }
        payload = {
            "countryCode": "",
            "email": EMAIL,
        }
        data = {"postData": json.dumps(payload, separators=(",", ":"))}
        
        try:
            resp = requests.post(endpoint, params=params, data=data, timeout=10)
            result = resp.json()
            print(f"  {name}: success={result.get('success')}, error={result.get('errorCode', 'none')}, msg={result.get('errorMsg', 'none')}")
            if result.get('success') and result.get('result') is not None:
                print(f"    Result: {result.get('result')}")
        except Exception as e:
            print(f"  {name}: {type(e).__name__}: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("LAMPUX OEM API RECONNAISSANCE")
    print("Read-only probing — no exploitation")
    print("=" * 60)
    
    probe_app_info()
    probe_user_exists()
    
    print("\n=== Probing token creation per region ===")
    for name, endpoint in REGIONS.items():
        probe_region(name, endpoint)
    
    probe_openapi_endpoints()
    
    print("\n\nDONE")
