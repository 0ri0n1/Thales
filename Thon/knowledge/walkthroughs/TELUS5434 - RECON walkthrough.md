# Skeleton Key Walkthrough — TELUS T3200M (192.168.1.254)

**Date:** 2026-03-08 05:24 CST
**Operator:** Eddie (Thon)
**Skill:** [Skeleton Key](file:///E:/Thon/.agents/skills/skeleton_key/SKILL.md)
**Target:** Home router gateway at `192.168.1.254`

---

## Mission Summary

Created the Skeleton Key skill from scratch, then applied all 7 phases against the home TELUS T3200M modem/router to extract session tokens, map the full web UI, enumerate connected devices, and document the authentication architecture.

---

## Phase 1 — Browser Login

Navigated to `http://192.168.1.254/` and authenticated with `admin / k3gq6pc3`. The dashboard confirmed: **"You are currently logged in as: admin"**.

````carousel
![Login page before authentication](C:\Users\Dallas\.gemini\antigravity\brain\e9a11334-3dbf-4dcd-9626-f6fc329b70d6\initial_login_page_1772969499929.png)
<!-- slide -->
![Authenticated dashboard](C:\Users\Dallas\.gemini\antigravity\brain\e9a11334-3dbf-4dcd-9626-f6fc329b70d6\post_login_dashboard_1772969523758.png)
````

![Login and authentication recording](C:\Users\Dallas\.gemini\antigravity\brain\e9a11334-3dbf-4dcd-9626-f6fc329b70d6\router_login_auth_1772969488365.webp)

---

## Phase 2 — Recon: Device Identification

| Field | Value |
|-------|-------|
| **Brand** | TELUS |
| **Model** | T3200M |
| **Serial** | GTBA7240105434 |
| **MAC** | 10:78:5B:FA:3C:11 |
| **Firmware** | 31.164L.22 |
| **WAN Type** | DSL (VDSL2 - 8B) |
| **WAN IP** | 162.157.135.240 |
| **Subnet** | 255.255.255.0 |
| **Gateway** | 162.157.135.1 |
| **DNS 1** | 75.153.171.67 |
| **DNS 2** | 75.153.171.124 |
| **System Uptime** | 4d 8h 9m |
| **DSL Link Uptime** | 0d 3h 14m |
| **SSID** | TELUS5434 |
| **Security** | WPA2-AES |
| **SmartSteering** | Enabled (2.4G + 5G) |
| **UPnP** | Enabled |
| **Firewall** | NAT Only |
| **Blocking/Filtering** | Disabled |

---

## Phase 3 — Token Extraction

| Storage | Key | Value |
|---------|-----|-------|
| **sessionStorage** | `sessionid` | `597981985` |
| **sessionStorage** | session key (discovered later) | `693869506` |
| **Cookie** | `css_js_update` | `20160406_telus` |
| **localStorage** | — | Empty |
| **Framework globals** | `__NEXT_DATA__`, `__NUXT__`, etc. | None detected |

> [!IMPORTANT]
> The T3200M uses **session-based cookie/sessionStorage auth**, not JWT/Bearer tokens. The `sessionid` in sessionStorage is the primary session credential. No refresh tokens exist — session expires on logout or idle timeout.

---

## Phase 4 — API Discovery & Protocol ID

### Architecture

The T3200M uses a **traditional multi-page HTML architecture** — no SPA framework, no REST API, no GraphQL. Full page reloads on every navigation click.

| Component | Detail |
|-----------|--------|
| **Rendering** | Server-side HTML |
| **Navigation** | `goThere('page.html')` JS function |
| **Session Keep-alive** | XHR poll to `./connect_left_refresh.html` every 3s |
| **Scripts** | `functions.js`, `nav.js`, `htmldecode.js`, `util.js` |
| **Endpoint Format** | Static `.html` pages (no `.cgi`, `.api`, `.json` detected) |

### Protocol Classification: **Traditional HTML Forms + Session Cookie**

No modern API layer exists. All configuration changes are submitted via HTML `<form>` POSTs. The interceptor captured no fetch/XHR API calls beyond the session keep-alive poll.

---

## Phase 5 — Full Web UI Navigation Map

### Top-Level Modules

| Module | URL |
|--------|-----|
| **Home** | `index.html` |
| **Status** | `modemstatus_home.html` |
| **Wireless Setup** | `wirelesssetup_basic.html` |
| **Firewall** | `advancedsetup_firewallsettings.html` |
| **Advanced Setup** | `advancedsetup_servicesblocking.html` *(warning bypass required)* |

### Status Sub-Pages (Sidebar)

**Internet Services:**
- Connection Status — `modemstatus_home.html`
- Line 1 Status — `modemstatus_wanstatus.html`
- Line 2 Status — (secondary DSL, inactive)
- WAN Ethernet Status
- Routing Table
- Firewall Status

**LAN Services:**
- NAT Table
- Wireless Status
- Modem Utilization
- LAN Status

**System Monitor:**
- ARP Table
- Network Devices Table — `connectedhome.html`
- Interface Statistics
- Multicast Statistics
- System Log — `advancedutilities_systemlog.html`

### Advanced Setup Sub-Pages

**Blocking/Filtering:** Services, Websites, Scheduling
**IP Address:** WAN/LAN IP, IPv6, DHCP Reservations, Port Bridging
**Modem Utilities:** Speed Test, Iperf, Ping, Traceroute, xDSL Diagnostics, Port Mirroring (Tool Box)

---

## Phase 6 — Connected Device Enumeration

````carousel
![Status — Line 1 DSL details](C:\Users\Dallas\.gemini\antigravity\brain\e9a11334-3dbf-4dcd-9626-f6fc329b70d6\line1_status_page_1772969810815.png)
<!-- slide -->
![Network Devices Table — all connected clients](C:\Users\Dallas\.gemini\antigravity\brain\e9a11334-3dbf-4dcd-9626-f6fc329b70d6\network_devices_table_1772969826739.png)
````

| Device | Connection | IP | MAC | Band |
|--------|------------|----|-----|------|
| iPhone | Wireless | 192.168.1.78 | 66:e2:1f:5e:27:f3 | 5G |
| DESKTOP-9IHNBQC | Wireless | 192.168.1.73 | 04:ec:d8:a2:ed:de | 5G |
| StreamingStick4K-M3 | Wireless | 192.168.1.66 | bc:d7:d4:69:68:da | 5G |
| Unknown | Wireless | 192.168.1.65 | 80:f3:ef:9e:ff:fe | 5G |
| Google-Home-Mini | Wireless | 192.168.1.70 | 20:df:b9:ce:f4:74 | 5G |
| Unknown | Wireless | 192.168.1.67 | a0:36:bc:4e:73:b9 | 2.4G |
| Unknown (Ethernet) | Ethernet | 192.168.1.64 | cc:28:aa:66:30:08 | Port 0 · 1000 Mbps Full |
| Unknown | Wireless | 192.168.1.75 | bc:89:a6:63:68:d9 | 2.4G |
| Unknown | Wireless | 192.168.1.74 | ac:fa:e4:ea:1a:e2 | 2.4G |
| Unknown | Wireless | 192.168.1.79 | 24:df:6a:a9:36:06 | 2.4G |
| 43onnRokuTV | Wireless | 192.168.1.68 | — | — |

**1 Ethernet** + **9 Wireless** = **10 active clients**

---

## Phase 7 — API Handoff Specification

```yaml
target: TELUS T3200M Gateway
address: 192.168.1.254
auth_type: session_cookie
session_storage_key: sessionid
session_value: "597981985"
session_key: "693869506"
cookie: "css_js_update=20160406_telus"
keep_alive_endpoint: "./connect_left_refresh.html"
keep_alive_interval: 3000ms
protocol: HTTP (no TLS)
api_style: HTML forms (no REST/GraphQL)
navigation_function: "goThere('page.html')"
firmware: "31.164L.22"
```

> [!CAUTION]
> This router has **no HTTPS** — all admin credentials and session tokens traverse the network in cleartext. Any device on the LAN can sniff the admin password.

---

## Skill Created

The Skeleton Key skill was created as a reusable agent pattern:

- [SKILL.md](file:///E:/Thon/.agents/skills/skeleton_key/SKILL.md) — Full 7-phase workflow with JS extraction snippets, network interceptor, and verification procedures

---

## Recordings

![Full token extraction and navigation walkthrough](C:\Users\Dallas\.gemini\antigravity\brain\e9a11334-3dbf-4dcd-9626-f6fc329b70d6\router_token_extraction_1772969589937.webp)

![About and UI deep exploration](C:\Users\Dallas\.gemini\antigravity\brain\e9a11334-3dbf-4dcd-9626-f6fc329b70d6\router_about_exploration_1772969763970.webp)
