---
name: Skeleton Key
description: Web app token extraction subagent — extracts auth tokens from browser sessions and maps undocumented APIs
---

# Skeleton Key: Web App Token Extraction Subagent

Skeleton Key is a specialized subagent pattern for extracting authentication tokens from web applications and reverse-engineering their API endpoints via authenticated browser sessions.

> [!IMPORTANT]
> Operates **ONLY** under owner authorization to access the owner's own data and services.

## Phased Workflow

### Phase 1 — Recon
Identify login portals, subdomains (`app.`, `dashboard.`, `portal.`), and any official API docs.

### Phase 2 — Browser Login
Open the target in a browser subagent. Authenticate using provided credentials or instruct the owner to log in manually. Wait until the authenticated dashboard/landing page is fully loaded.

### Phase 3 — Token Extraction
Execute the following JavaScript snippets in the browser console to locate auth tokens:

**Full localStorage dump:**
```javascript
(function() {
  const all = {};
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    const val = localStorage.getItem(key);
    all[key] = val && val.length > 500 ? val.substring(0, 500) + '...' : val;
  }
  return JSON.stringify(all, null, 2);
})()
```

**Full sessionStorage dump:**
```javascript
(function() {
  const all = {};
  for (let i = 0; i < sessionStorage.length; i++) {
    const key = sessionStorage.key(i);
    const val = sessionStorage.getItem(key);
    all[key] = val && val.length > 500 ? val.substring(0, 500) + '...' : val;
  }
  return JSON.stringify(all, null, 2);
})()
```

**Cookie dump:**
```javascript
document.cookie
```

**Framework globals check:**
```javascript
JSON.stringify(window.__NEXT_DATA__ || window.__NUXT__ || window.__APP_DATA__ || 'none')
```

**Known service-specific keys:**

| Service      | Key                                 | Notes      |
| ------------ | ----------------------------------- | ---------- |
| Hack The Box | `localStorage['htb-token']`         | JWT        |
| Plaud AI     | `localStorage['tokenstr']`          | Raw bearer |
| Beside       | `localStorage['beside_auth_token']` | Auth token |

**Look for:** `token`, `auth`, `session`, `access`, `jwt`, `bearer`, `credential`, or values starting with `eyJ` (base64 JWT header).

> [!CAUTION]
> **Double-Prefix Trap:** Some apps store the token already prefixed with `Bearer `. Always inspect the raw value before adding a prefix in scripts.

### Phase 4 — API Discovery (Network Interceptor)
Install a fetch/XHR interceptor to capture outgoing requests:

```javascript
(function() {
  window._skCapture = [];
  const origFetch = window.fetch;
  window.fetch = function(...args) {
    const req = args[0], opts = args[1] || {};
    let url = typeof req === 'string' ? req : (req instanceof Request ? req.url : String(req));
    let headers = {};
    if (opts.headers) {
      if (opts.headers instanceof Headers) opts.headers.forEach((v,k) => { headers[k] = v; });
      else if (typeof opts.headers === 'object') headers = {...opts.headers};
    }
    if (req instanceof Request) req.headers.forEach((v,k) => { headers[k] = v; });
    window._skCapture.push({ url, method: opts.method || 'GET', headers,
      bodyType: opts.body ? opts.body.constructor.name : 'none' });
    return origFetch.apply(this, args);
  };
  const origOpen = XMLHttpRequest.prototype.open;
  const origSet = XMLHttpRequest.prototype.setRequestHeader;
  XMLHttpRequest.prototype.open = function(m, u, ...r) {
    this._m = m; this._u = u; this._h = {};
    return origOpen.apply(this, [m, u, ...r]);
  };
  XMLHttpRequest.prototype.setRequestHeader = function(k, v) {
    if (this._h) this._h[k] = v;
    return origSet.apply(this, [k, v]);
  };
  const origSend = XMLHttpRequest.prototype.send;
  XMLHttpRequest.prototype.send = function(body) {
    window._skCapture.push({ url: this._u, method: this._m, headers: this._h, type: 'xhr' });
    return origSend.apply(this, [body]);
  };
  return 'Interceptor active';
})()
```

Navigate the app to trigger API calls, then dump captured traffic:
```javascript
JSON.stringify(window._skCapture, null, 2)
```

### Phase 5 — Protocol Identification
Classify the API type based on captured traffic:

| Indicator                                | Protocol  |
| ---------------------------------------- | --------- |
| `/api/v*` paths, JSON responses          | REST      |
| `/graphql` path, `query`/`mutation` body | GraphQL   |
| `application/grpc-web`, proto payloads   | gRPC-Web  |
| `wss://` connections                     | WebSocket |

### Phase 6 — Verification
Test extracted credentials via CLI (Python `requests`):

```python
import requests
TOKEN = "<extracted_token>"
headers = {
    "Authorization": f"Bearer {TOKEN}",  # adjust prefix as needed
    "Content-Type": "application/json",
    "Origin": "https://<app-domain>",
    "Referer": "https://<app-domain>/",
}
r = requests.get("https://<api_endpoint>", headers=headers)
print(r.status_code, r.text[:500])
```

### Phase 7 — API Handoff
Produce a structured technical specification documenting:
- Authentication format and token location
- Token renewal/refresh instructions
- Base URLs and API version
- Required headers (`Origin`, `Referer`, `Authorization`)
- Key endpoints with methods and example payloads

## Output Artifacts
Store results in `reports/skeleton_key_<target>.md` with:
1. Target summary
2. Extracted credentials (redacted for safety)
3. Full API endpoint map
4. Verification proof (HTTP status codes, response snippets)
