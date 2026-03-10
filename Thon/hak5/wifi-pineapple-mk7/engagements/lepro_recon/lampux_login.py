#!/usr/bin/env python3
import functools
import hmac
import hashlib
import json
import requests
import time
import sys

_TUYA_USER_AGENT = "TY-UA=APP/Android/1.1.6/SDK/null"
_TUYA_API_VERSION = "1.0"

class TuyaOEM:
    def __init__(self, region, username, password, client_id, secret):
        self._endpoint = f"https://a1.tuya{region}.com/api.json"
        self._username = username
        self._password = password
        self._country_code = ""
        self._client_id = client_id
        self._secret = secret
        self._session = requests.session()
        self._sid = None

    def _api(self, action, payload=None, extra_params=None, requires_sid=True):
        headers = {"User-Agent": _TUYA_USER_AGENT}
        if extra_params is None:
            extra_params = {}
        params = {
            "a": action,
            "clientId": self._client_id,
            "v": _TUYA_API_VERSION,
            "time": str(int(time.time())),
            **extra_params,
        }
        if requires_sid:
            if self._sid is None:
                raise ValueError("Login first")
            params["sid"] = self._sid
        data = {}
        if payload is not None:
            data["postData"] = json.dumps(payload, separators=(",", ":"))
        params["sign"] = self._sign({**params, **data})
        result = self._session.post(self._endpoint, params=params, data=data, headers=headers)
        return result.json()

    def _sign(self, data):
        keys_not_to_sign = ["gid"]
        sorted_keys = sorted(list(data.keys()))
        str_to_sign = ""
        for key in sorted_keys:
            if key in keys_not_to_sign:
                continue
            if key == "postData":
                if len(str_to_sign) > 0:
                    str_to_sign += "||"
                str_to_sign += key + "=" + self._mobile_hash(data[key])
            else:
                if len(str_to_sign) > 0:
                    str_to_sign += "||"
                str_to_sign += key + "=" + data[key]
        return hmac.new(
            bytes(self._secret, "utf-8"),
            msg=bytes(str_to_sign, "utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()

    @staticmethod
    def _mobile_hash(data):
        prehash = hashlib.md5(bytes(data, "utf-8")).hexdigest()
        return prehash[8:16] + prehash[0:8] + prehash[24:32] + prehash[16:24]

    @staticmethod
    def _plain_rsa_encrypt(modulus, exponent, message):
        message_int = int.from_bytes(message, "big")
        enc_message_int = pow(message_int, exponent, modulus)
        return enc_message_int.to_bytes(256, "big")

    def _enc_password(self, modulus, exponent, password):
        passwd_hash = hashlib.md5(password.encode("utf8")).hexdigest().encode("utf8")
        return self._plain_rsa_encrypt(int(modulus), int(exponent), passwd_hash).hex()

    def login(self):
        payload = {"countryCode": self._country_code, "email": self._username}
        result = self._api("tuya.m.user.email.token.create", payload, requires_sid=False)
        print(f"  Token response: success={result.get('success')}, errorCode={result.get('errorCode', 'none')}, errorMsg={result.get('errorMsg', 'none')}")
        if not result.get("success"):
            return False
        token_info = result["result"]
        payload = {
            "countryCode": self._country_code,
            "email": self._username,
            "ifencrypt": 1,
            "options": '{"group": 1}',
            "passwd": self._enc_password(token_info["publicKey"], token_info["exponent"], self._password),
            "token": token_info["token"],
        }
        login_result = self._api("tuya.m.user.email.password.login", payload, requires_sid=False)
        print(f"  Login response: success={login_result.get('success')}, errorCode={login_result.get('errorCode', 'none')}")
        if login_result.get("success"):
            self._sid = login_result["result"]["sid"]
            return True
        return False

    def list_devices(self):
        groups = self._api("tuya.m.location.list")
        if not groups.get("success"):
            print(f"  Groups failed: {groups}")
            return []
        devs = []
        for group in groups["result"]:
            dev_result = self._api("tuya.m.my.group.device.list", extra_params={"gid": group["groupId"]})
            if dev_result.get("success"):
                for dev in dev_result["result"]:
                    devs.append({
                        "name": dev.get("name"),
                        "id": dev.get("devId"),
                        "local_key": dev.get("localKey"),
                        "mac": dev.get("mac"),
                        "uuid": dev.get("uuid"),
                        "category": dev.get("category"),
                        "product_id": dev.get("productId"),
                        "ip": dev.get("ip"),
                        "dps": dev.get("dps"),
                    })
        return devs


EMAIL = "dallaskappel@gmail.com"
PASSWORD = "Y0urmom69!"
CLIENT_ID = "h5gw8q4artygy784ww4v"
APP_SECRET = "n3s33y3j8dsy5vm4kea75p55gn3ycsdy"
CERT_HASH = "37:95:F5:F7:C6:4D:79:B2:37:54:02:DD:9E:69:32:DA:38:0E:BA:8A:1E:17:94:56:25:B7:6C:7C:60:CD:63:12"

secret_patterns = [
    ("A_appsecret_appsecret", f"A_{APP_SECRET}_{APP_SECRET}"),
    ("cert_appsecret_appsecret", f"{CERT_HASH}_{APP_SECRET}_{APP_SECRET}"),
    ("raw appsecret", APP_SECRET),
]

for region in ["us", "eu"]:
    for name, secret in secret_patterns:
        print(f"\n=== Region={region}, Pattern='{name}' ===")
        try:
            api = TuyaOEM(region, EMAIL, PASSWORD, CLIENT_ID, secret)
            if api.login():
                print(f"  SUCCESS! SID: {api._sid}")
                devs = api.list_devices()
                print(f"  Found {len(devs)} devices:")
                print(json.dumps(devs, indent=2))
                with open('/tmp/lampux_devices.json', 'w') as f:
                    json.dump(devs, f, indent=2)
                print("  Saved to /tmp/lampux_devices.json")
                sys.exit(0)
            else:
                print("  Login failed")
        except Exception as e:
            print(f"  Error: {type(e).__name__}: {e}")

print("\n\nAll patterns exhausted.")
