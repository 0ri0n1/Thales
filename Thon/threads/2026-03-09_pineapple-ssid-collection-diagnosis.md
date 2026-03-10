# Pineapple MK7 SSID Collection Failure: Firmware JSON Bug Diagnosis and UCI Fix

**Date:** 2026-03-09
**Operator:** Thon (Venom)
**Authority:** Eddie (Sovereign)
**Equipment:** WiFi Pineapple Mark 7, FW 2.1.3
**Classification:** Diagnostic / Remediation

---

## Problem Statement

Eddie reported the Pineapple was not collecting SSIDs. Web UI displayed error on PineAP settings save:

```
json: cannot unmarshal string into Go struct field PineAPSettings.settings.karma of type bool
```

## Root Cause

Type mismatch bug in MK7 firmware v2.1.3. The Go backend (`/pineapple/pineapple`) expects `karma` as a boolean (`true`/`false`), but the web UI serializes it as a string (`"0"`). The API rejects the entire JSON payload on save, so all PineAP settings silently fail to persist.

Runtime config (`/tmp/pineap.conf`) regenerated from UCI defaults at each daemon restart with all collection features set to `off`.

## Diagnostic Chain

1. **SSH connectivity** — Pineapple reachable at 172.16.42.1 (ping OK)
2. **SSH auth failure** — Kali container's ed25519 key not in Pineapple `authorized_keys`. Password auth (`Mousepad7`) still works.
3. **PineAP daemon running** — Web UI responsive on port 1471, `pineapd` and `/pineapple/pineapple` both alive
4. **UCI config showed all features OFF:**
   - `capture_ssids='off'`
   - `broadcast_ssid_pool='off'`
   - `beacon_responses='off'`
   - `logging='off'`
5. **Runtime config (`/tmp/pineap.conf`) confirmed OFF** — generated from UCI at daemon startup
6. **API endpoints returned `{"error":"Error"}`** — same JSON marshal bug affecting all settings endpoints
7. **Monitor interface conflict** — wlan1 and wlan1mon both in monitor mode on same phy (duplicate)
8. **Channel locked** — wlan1mon stuck on channel 11, no hopping
9. **Databases NOT empty** — `sqlite3` not installed on Pineapple; DB analysis done by SCP to Kali container
10. **`pineap.log` flat file never created** — Go daemon responsible for this file, bug prevents it

## Actual Data State (at diagnosis)

| Database | Contents |
|----------|----------|
| recon.db (1.7MB) | 308 APs, 13,203 clients |
| log.db (2.0MB) | 41,578 probe entries (62 in last 5 min — actively writing) |
| pineapple.db | 68 SSIDs in pool |
| filters.db | 3 MAC deny (TELUS5434 gateway), 2 SSID deny (TELUS5434, TELUS5434_RPT) |

Unique probed SSIDs captured: **111**

## Remediation Applied

1. **PineAP config set via UCI** (bypasses broken web UI):
   ```
   uci set pineap.@config[0].capture_ssids='on'
   uci set pineap.@config[0].broadcast_ssid_pool='on'
   uci set pineap.@config[0].beacon_responses='on'
   uci set pineap.@config[0].logging='on'
   uci commit pineap
   ```
2. **Monitor interface cleaned** — removed duplicate wlan1/wlan1mon, recreated via `airmon-ng start wlan1`
3. **Daemons restarted** — `/etc/init.d/pineapd restart` + `/etc/init.d/pineapple restart` to regenerate `pineap.conf` from updated UCI
4. **SSH key re-provisioned** — Kali ed25519 key added to Pineapple `authorized_keys`
5. **Verified** — `pineap.conf` confirmed showing all features `on`; beacons observed via tcpdump broadcasting pool SSIDs

## Remaining Issues

- **`pineap.log` flat file** not created — Go daemon JSON bug prevents it. The SSID harvester script (`scripts/ssid_harvester.sh`) relies on this file. Should be adapted to query `log.db` directly.
- **Channel hopping** — `pineapd` locks to `ap_channel` and does not hop autonomously. Recon scans (via API or script) handle multi-channel sweeps separately.
- **Web UI save** — broken until Hak5 patches firmware. All config changes must go through UCI + init.d restart.
- **`sqlite3` not installed** on Pineapple — DB queries require SCP to Kali or opkg install.

## Key Learnings

1. The MK7 web UI can show settings as "enabled" while the backend silently rejects the save. Always verify via `uci show pineap` or `cat /tmp/pineap.conf`.
2. `pineapd` reads `pineap.conf` only at startup. UCI changes require daemon restart to take effect.
3. The `pineapd_wrapper` script generates `pineap.conf` from UCI, creates the monitor interface, then launches `pineapd`. This is the correct restart path.
4. Databases are the source of truth for collection data, not flat log files.

## Scripts Created

| Script | Purpose |
|--------|---------|
| `scripts/diag_full.sh` | Full diagnostic (interfaces, processes, config, logs) |
| `scripts/fix_pineap.sh` | UCI config fix + daemon restart |
| `scripts/fix_ssh_key2.sh` | SSH key provisioning |
| `scripts/verify_capture.sh` | Post-fix capture verification |
| `scripts/check_capture.sh` | SCP databases to Kali for analysis |

---

*Thread archived by Thon — 2026-03-09*
