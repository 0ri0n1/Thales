#!/usr/bin/env bash
###############################################################################
# pineapple_recon.sh — Automated WiFi Pineapple Wireless Reconnaissance
#
# Operator: Thon (Venom/Agent)
# Authority: Eddie (Sovereign/Principal)
# Classification: RECON ONLY — no offensive operations
#
# This script runs inside the Kali Docker container (kali-mcp-pentest) and
# automates the complete wireless recon workflow:
#   1. Home device enumeration & deny list push
#   2. Passive wireless scanning (airodump-ng)
#   3. Probe request capture
#   4. OUI vendor lookups
#   5. Markdown report generation
#
# Prerequisites:
#   - WiFi Pineapple Mark 7 reachable at $PINE_IP via SSH
#   - Monitor mode interface active (wlan1mon)
#   - sshpass and sqlite3 installed in the Kali container
#   - Host computer on the home WiFi network
#
# Usage (from Kali container):
#   ./pineapple_recon.sh
#   ./pineapple_recon.sh --scan-duration 120 --skip-denylist
#   ./pineapple_recon.sh --help
#
# Usage (from Windows host):
#   powershell -File E:\Thon\scripts\run_recon.ps1
###############################################################################
set -euo pipefail

#=============================================================================
# Configuration — edit these to match your environment
#=============================================================================
PINE_IP="${PINE_IP:-172.16.42.1}"
PINE_USER="${PINE_USER:-root}"
PINE_PASS="${PINE_PASS:-Mousepad7}"
PINE_MON_IF="${PINE_MON_IF:-wlan1mon}"       # Monitor mode interface
PINE_CLIENT_IF="${PINE_CLIENT_IF:-wlan2}"    # Client radio
PINE_BAND="${PINE_BAND:-bg}"                 # Scan band (bg = 2.4GHz, a = 5GHz, abg = both)
HOME_SUBNET="${HOME_SUBNET:-192.168.1}"      # First 3 octets of home subnet
HOME_SSIDS="${HOME_SSIDS:-TELUS5434,TELUS5434_RPT}"  # Comma-separated home SSIDs

# Scan parameters
SCAN_DURATION="${SCAN_DURATION:-90}"          # Seconds for airodump-ng channel hop
CHANNEL_DWELL="${CHANNEL_DWELL:-30}"          # Seconds per targeted channel capture
PROBE_CAPTURE_PKTS="${PROBE_CAPTURE_PKTS:-500}" # Packets for probe request capture

# Output
REPORT_DIR="${REPORT_DIR:-/tmp/recon_output}"
TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)
REPORT_FILE="${REPORT_DIR}/wireless_recon_${TIMESTAMP}.md"
RAW_DIR="${REPORT_DIR}/raw_${TIMESTAMP}"

# Flags
SKIP_DENYLIST=false
SKIP_SCAN=false
VERBOSE=false

#=============================================================================
# Argument Parsing
#=============================================================================
print_help() {
    cat <<'HELP'
Usage: pineapple_recon.sh [OPTIONS]

Options:
  --pine-ip IP           Pineapple IP (default: 172.16.42.1)
  --pine-pass PASS       Pineapple SSH password (default: Mousepad7)
  --scan-duration SECS   Airodump channel-hop duration (default: 90)
  --channel-dwell SECS   Per-channel targeted capture (default: 30)
  --probe-pkts NUM       Packet count for probe capture (default: 500)
  --band BAND            Scan band: bg, a, abg (default: bg)
  --home-subnet PREFIX   First 3 octets of home subnet (default: 192.168.1)
  --home-ssids LIST      Comma-separated home SSIDs (default: TELUS5434,TELUS5434_RPT)
  --report-dir DIR       Output directory (default: /tmp/recon_output)
  --skip-denylist        Skip deny list push (use if already configured)
  --skip-scan            Skip wireless scanning (report from existing data only)
  --verbose              Enable verbose output
  --help                 Show this help
HELP
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --pine-ip)      PINE_IP="$2"; shift 2 ;;
        --pine-pass)    PINE_PASS="$2"; shift 2 ;;
        --scan-duration) SCAN_DURATION="$2"; shift 2 ;;
        --channel-dwell) CHANNEL_DWELL="$2"; shift 2 ;;
        --probe-pkts)   PROBE_CAPTURE_PKTS="$2"; shift 2 ;;
        --band)         PINE_BAND="$2"; shift 2 ;;
        --home-subnet)  HOME_SUBNET="$2"; shift 2 ;;
        --home-ssids)   HOME_SSIDS="$2"; shift 2 ;;
        --report-dir)   REPORT_DIR="$2"; shift 2 ;;
        --skip-denylist) SKIP_DENYLIST=true; shift ;;
        --skip-scan)    SKIP_SCAN=true; shift ;;
        --verbose)      VERBOSE=true; shift ;;
        --help)         print_help; exit 0 ;;
        *)              echo "Unknown option: $1"; print_help; exit 1 ;;
    esac
done

#=============================================================================
# Utility Functions
#=============================================================================
SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=10"

pine_ssh() {
    sshpass -p "$PINE_PASS" ssh $SSH_OPTS "${PINE_USER}@${PINE_IP}" "$@"
}

pine_scp_get() {
    sshpass -p "$PINE_PASS" scp $SSH_OPTS "${PINE_USER}@${PINE_IP}:$1" "$2"
}

pine_scp_put() {
    sshpass -p "$PINE_PASS" scp $SSH_OPTS "$1" "${PINE_USER}@${PINE_IP}:$2"
}

log() {
    echo "[$(date +%H:%M:%S)] $*"
}

log_verbose() {
    if $VERBOSE; then
        echo "[$(date +%H:%M:%S)] [VERBOSE] $*"
    fi
}

die() {
    echo "[FATAL] $*" >&2
    exit 1
}

section() {
    echo ""
    echo "================================================================="
    echo "  $*"
    echo "================================================================="
}

#=============================================================================
# Preflight Checks
#=============================================================================
preflight() {
    section "PREFLIGHT CHECKS"

    # Check required tools
    for tool in sshpass sqlite3 python3; do
        if ! command -v "$tool" &>/dev/null; then
            die "Required tool not found: $tool"
        fi
        log "✓ $tool available"
    done

    # Test Pineapple SSH connectivity
    log "Testing SSH to Pineapple at ${PINE_IP}..."
    if ! pine_ssh "echo OK" 2>/dev/null | grep -q "OK"; then
        die "Cannot SSH to Pineapple at ${PINE_IP}"
    fi
    log "✓ SSH connection to Pineapple OK"

    # Check monitor interface exists
    log "Checking monitor interface ${PINE_MON_IF}..."
    if ! pine_ssh "ip link show ${PINE_MON_IF}" &>/dev/null; then
        die "Monitor interface ${PINE_MON_IF} not found on Pineapple"
    fi
    log "✓ Monitor interface ${PINE_MON_IF} exists"

    # Get Pineapple firmware version
    local fw
    fw=$(pine_ssh "cat /etc/pineapple/version 2>/dev/null || echo unknown")
    log "  Pineapple firmware: $fw"

    # Create output directories
    mkdir -p "$REPORT_DIR" "$RAW_DIR"
    log "✓ Output directory: $REPORT_DIR"
}

#=============================================================================
# Phase 1: Home Device Enumeration
#=============================================================================
# This function accepts a file of MAC addresses (one per line) as input.
# When called from the PowerShell launcher, it receives the Windows ARP table.
# When called standalone, it reads from an existing file or the Pineapple's ARP.

enumerate_home_devices() {
    section "PHASE 1: HOME DEVICE ENUMERATION"

    local mac_file="${RAW_DIR}/home_macs.txt"
    local home_devices_file="${RAW_DIR}/home_devices.csv"

    # Check if home MACs were provided by the launcher
    if [[ -f "${REPORT_DIR}/home_arp_input.csv" ]]; then
        log "Using home device list from launcher..."
        cp "${REPORT_DIR}/home_arp_input.csv" "$home_devices_file"
    else
        log "No home ARP input found. Scanning Pineapple ARP table as fallback..."
        # Fallback: get what the Pineapple can see via its client radio
        pine_ssh "ip neigh show dev ${PINE_CLIENT_IF} 2>/dev/null || echo ''" > "$home_devices_file"
    fi

    # Extract unique MACs
    grep -oiE '([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}' "$home_devices_file" | \
        tr '[:lower:]' '[:upper:]' | \
        tr '-' ':' | \
        sort -u > "$mac_file"

    local mac_count
    mac_count=$(wc -l < "$mac_file")
    log "Found $mac_count unique home device MACs"

    # Also add AP BSSIDs for the home network (from iwinfo scan)
    log "Scanning for home AP BSSIDs via iwinfo..."
    local iwinfo_raw="${RAW_DIR}/iwinfo_scan.txt"
    pine_ssh "iwinfo ${PINE_CLIENT_IF} scan 2>/dev/null" > "$iwinfo_raw" || true

    # Extract BSSIDs associated with home SSIDs
    IFS=',' read -ra SSID_ARRAY <<< "$HOME_SSIDS"
    for ssid in "${SSID_ARRAY[@]}"; do
        local bssids
        bssids=$(grep -B5 "ESSID: \"${ssid}\"" "$iwinfo_raw" 2>/dev/null | \
                 grep -oiE '([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}' | \
                 tr '[:lower:]' '[:upper:]' || true)
        if [[ -n "$bssids" ]]; then
            echo "$bssids" >> "$mac_file"
            log "  Found BSSID(s) for ${ssid}: $(echo "$bssids" | tr '\n' ' ')"
        fi
    done

    # Deduplicate final MAC list
    sort -u "$mac_file" -o "$mac_file"
    mac_count=$(wc -l < "$mac_file")
    log "Total unique MACs for deny list: $mac_count"

    cat "$mac_file"
    echo ""
}

#=============================================================================
# Phase 1b: Deny List Push
#=============================================================================
push_denylist() {
    section "PHASE 1b: DENY LIST CONFIGURATION"

    if $SKIP_DENYLIST; then
        log "Skipping deny list push (--skip-denylist flag set)"
        return 0
    fi

    local mac_file="${RAW_DIR}/home_macs.txt"
    local local_db="/tmp/filters_work_${TIMESTAMP}.db"

    if [[ ! -f "$mac_file" ]] || [[ ! -s "$mac_file" ]]; then
        log "WARNING: No home MACs found. Skipping deny list push."
        return 0
    fi

    # Pull current filters.db from Pineapple
    log "Pulling filters.db from Pineapple..."
    pine_scp_get "/etc/pineapple/filters.db" "$local_db"

    # Count existing entries
    local existing_macs existing_ssids
    existing_macs=$(sqlite3 "$local_db" "SELECT COUNT(*) FROM mac_filter_list;" 2>/dev/null || echo "0")
    existing_ssids=$(sqlite3 "$local_db" "SELECT COUNT(*) FROM ssid_filter_list;" 2>/dev/null || echo "0")
    log "Existing filters: $existing_macs MACs, $existing_ssids SSIDs"

    # Insert MACs
    log "Inserting home device MACs..."
    while IFS= read -r mac; do
        [[ -z "$mac" ]] && continue
        mac=$(echo "$mac" | tr '[:lower:]' '[:upper:]' | xargs)
        sqlite3 "$local_db" "INSERT OR IGNORE INTO mac_filter_list (mac) VALUES ('${mac}');"
        log_verbose "  Inserted MAC: $mac"
    done < "$mac_file"

    # Insert SSIDs
    log "Inserting home SSIDs..."
    IFS=',' read -ra SSID_ARRAY <<< "$HOME_SSIDS"
    for ssid in "${SSID_ARRAY[@]}"; do
        sqlite3 "$local_db" "INSERT OR IGNORE INTO ssid_filter_list (ssid) VALUES ('${ssid}');"
        log "  Inserted SSID: $ssid"
    done

    # Count after insertion
    local new_macs new_ssids
    new_macs=$(sqlite3 "$local_db" "SELECT COUNT(*) FROM mac_filter_list;")
    new_ssids=$(sqlite3 "$local_db" "SELECT COUNT(*) FROM ssid_filter_list;")
    log "After insertion: $new_macs MACs, $new_ssids SSIDs"

    # Push back to Pineapple
    log "Pushing updated filters.db to Pineapple..."
    pine_scp_put "$local_db" "/etc/pineapple/filters.db"

    # Signal daemon to reload
    pine_ssh "killall -HUP pineapple 2>/dev/null || true"
    log "Signaled Pineapple daemon to reload filters"

    # Verify filter mode
    local mac_mode ssid_mode
    mac_mode=$(pine_ssh "uci get pineap.@config[0].mac_filter 2>/dev/null" || echo "unknown")
    ssid_mode=$(pine_ssh "uci get pineap.@config[0].ssid_filter 2>/dev/null" || echo "unknown")
    log "Filter modes — MAC: ${mac_mode}, SSID: ${ssid_mode}"

    if [[ "$mac_mode" != "black" ]]; then
        log "WARNING: MAC filter mode is '${mac_mode}', expected 'black' (deny). Setting..."
        pine_ssh "uci set pineap.@config[0].mac_filter=black; uci commit pineap"
    fi
    if [[ "$ssid_mode" != "black" ]]; then
        log "WARNING: SSID filter mode is '${ssid_mode}', expected 'black' (deny). Setting..."
        pine_ssh "uci set pineap.@config[0].ssid_filter=black; uci commit pineap"
    fi

    log "✓ Deny list configuration complete"

    # Save deny list snapshot to raw output
    sqlite3 "$local_db" "SELECT mac FROM mac_filter_list ORDER BY mac;" > "${RAW_DIR}/denylist_macs.txt"
    sqlite3 "$local_db" "SELECT ssid FROM ssid_filter_list ORDER BY ssid;" > "${RAW_DIR}/denylist_ssids.txt"

    # Cleanup temp DB
    rm -f "$local_db"
}

#=============================================================================
# Phase 2: Passive Wireless Scanning
#=============================================================================
wireless_scan() {
    section "PHASE 2: PASSIVE WIRELESS SCANNING"

    if $SKIP_SCAN; then
        log "Skipping wireless scan (--skip-scan flag set)"
        return 0
    fi

    local csv_file="${RAW_DIR}/airodump.csv"

    # Clean any previous scan files on Pineapple
    pine_ssh "rm -f /tmp/recon-01.* 2>/dev/null; rm -f /tmp/recon.csv 2>/dev/null"

    # Run airodump-ng with channel hopping
    log "Starting airodump-ng scan (${SCAN_DURATION}s, band: ${PINE_BAND})..."
    pine_ssh "
        airodump-ng ${PINE_MON_IF} --write /tmp/recon --output-format csv --band ${PINE_BAND} &>/dev/null &
        ADPID=\$!
        sleep ${SCAN_DURATION}
        kill \$ADPID 2>/dev/null
        wait \$ADPID 2>/dev/null
        sleep 1
    "

    # Pull results
    log "Retrieving scan results..."
    pine_ssh "cat /tmp/recon-01.csv 2>/dev/null || echo 'NO_DATA'" > "$csv_file"

    if grep -q "NO_DATA" "$csv_file"; then
        log "WARNING: No airodump data captured. Check monitor interface."
        return 1
    fi

    # Count results
    local ap_count client_count
    ap_count=$(grep -c '^[0-9A-Fa-f]' "$csv_file" 2>/dev/null | head -1 || echo "0")
    # Client section starts after the empty line + "Station MAC" header
    client_count=$(awk '/^Station MAC/{found=1; next} found && /^[0-9A-Fa-f]/' "$csv_file" | wc -l || echo "0")
    log "Captured: ~${ap_count} AP entries, ~${client_count} client entries"

    log "✓ Airodump scan complete"
}

#=============================================================================
# Phase 2b: Active AP Scan (iwinfo)
#=============================================================================
active_ap_scan() {
    section "PHASE 2b: ACTIVE AP SCAN (iwinfo)"

    local iwinfo_file="${RAW_DIR}/iwinfo_full.txt"

    log "Running iwinfo scan on ${PINE_CLIENT_IF}..."
    pine_ssh "iwinfo ${PINE_CLIENT_IF} scan 2>/dev/null" > "$iwinfo_file" || true

    local ap_count
    ap_count=$(grep -c "ESSID:" "$iwinfo_file" 2>/dev/null || echo "0")
    log "iwinfo found ${ap_count} APs"
    log "✓ Active AP scan complete"
}

#=============================================================================
# Phase 3: Probe Request Capture
#=============================================================================
capture_probes() {
    section "PHASE 3: PROBE REQUEST CAPTURE"

    if $SKIP_SCAN; then
        log "Skipping probe capture (--skip-scan flag set)"
        return 0
    fi

    local probes_file="${RAW_DIR}/probe_requests.txt"
    local tcpdump_raw="${RAW_DIR}/tcpdump_raw.txt"

    # Capture on most active channels
    for channel in 1 6 11; do
        log "Capturing probes on channel ${channel} (${CHANNEL_DWELL}s)..."
        pine_ssh "
            iw dev ${PINE_MON_IF} set channel ${channel} 2>/dev/null
            tcpdump -i ${PINE_MON_IF} -e -c ${PROBE_CAPTURE_PKTS} 2>&1
        " >> "$tcpdump_raw" 2>/dev/null || true
    done

    # Extract probe requests
    grep -i "Probe Request" "$tcpdump_raw" 2>/dev/null > "$probes_file" || true

    local probe_count
    probe_count=$(wc -l < "$probes_file" 2>/dev/null || echo "0")
    log "Captured $probe_count probe request frames"

    # Parse unique probing devices
    log "Unique probing devices:"
    grep -oiE 'SA:([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}' "$probes_file" 2>/dev/null | \
        sed 's/^SA://i' | sort -u | while read -r mac; do
            local probed_ssids
            probed_ssids=$(grep -i "$mac" "$probes_file" | \
                           grep -oP 'Probe Request \(\K[^)]+' | \
                           sort -u | tr '\n' ', ' | sed 's/,$//')
            echo "  $mac → ${probed_ssids:-broadcast}"
        done

    log "✓ Probe capture complete"
}

#=============================================================================
# Phase 4: OUI Vendor Lookups
#=============================================================================
oui_lookup() {
    section "PHASE 4: OUI VENDOR LOOKUPS"

    local oui_output="${RAW_DIR}/oui_lookups.csv"
    local all_macs="${RAW_DIR}/all_discovered_macs.txt"

    # Collect all unique MACs from all sources
    {
        grep -oiE '([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}' "${RAW_DIR}/airodump.csv" 2>/dev/null || true
        grep -oiE '([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}' "${RAW_DIR}/iwinfo_full.txt" 2>/dev/null || true
        grep -oiE '([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}' "${RAW_DIR}/probe_requests.txt" 2>/dev/null || true
        cat "${RAW_DIR}/home_macs.txt" 2>/dev/null || true
    } | tr '[:lower:]' '[:upper:]' | sort -u > "$all_macs"

    local mac_count
    mac_count=$(wc -l < "$all_macs")
    log "Looking up OUI for $mac_count unique MACs..."

    # Build Python lookup script
    local py_script="${RAW_DIR}/oui_lookup.py"
    cat > "$py_script" <<'PYEOF'
import json, sys
with open("/etc/pineapple/ouis") as f:
    oui = json.load(f)
for line in sys.stdin:
    mac = line.strip()
    if not mac:
        continue
    prefix = mac.replace(":", "")[:6].upper()
    vendor = oui.get(prefix, "UNKNOWN")
    # Check if locally administered (bit 1 of first octet)
    first_byte = int(prefix[:2], 16)
    if first_byte & 0x02:
        vendor = "Locally Administered"
    print(mac + "," + vendor)
PYEOF

    # Run OUI lookup on Pineapple
    pine_scp_put "$py_script" "/tmp/oui_lookup.py"
    pine_scp_put "$all_macs" "/tmp/all_macs.txt"
    pine_ssh "cat /tmp/all_macs.txt | python3 /tmp/oui_lookup.py" > "$oui_output"

    # Show results
    log "OUI Results:"
    while IFS=',' read -r mac vendor; do
        log "  $mac → $vendor"
    done < "$oui_output"

    log "✓ OUI lookups complete ($mac_count MACs resolved)"
}

#=============================================================================
# Phase 5: Parse & Analyze
#=============================================================================
parse_airodump() {
    section "PHASE 5: DATA PARSING & ANALYSIS"

    local csv_file="${RAW_DIR}/airodump.csv"
    local parsed_aps="${RAW_DIR}/parsed_aps.csv"
    local parsed_clients="${RAW_DIR}/parsed_clients.csv"

    if [[ ! -f "$csv_file" ]]; then
        log "No airodump data to parse"
        return 0
    fi

    # Parse APs section (before the blank line + Station MAC header)
    log "Parsing AP data..."
    awk '
    BEGIN { FS=","; in_ap=1 }
    /^Station MAC/ { in_ap=0; next }
    /^$/ { next }
    in_ap && /^[0-9A-Fa-f]/ {
        bssid=$1; channel=$4; speed=$5; privacy=$6; cipher=$7; auth=$8;
        power=$9; beacons=$10; ivs=$11; essid=$14
        # Trim whitespace
        gsub(/^[ \t]+|[ \t]+$/, "", bssid)
        gsub(/^[ \t]+|[ \t]+$/, "", channel)
        gsub(/^[ \t]+|[ \t]+$/, "", privacy)
        gsub(/^[ \t]+|[ \t]+$/, "", essid)
        gsub(/^[ \t]+|[ \t]+$/, "", power)
        gsub(/^[ \t]+|[ \t]+$/, "", beacons)
        gsub(/^[ \t]+|[ \t]+$/, "", ivs)
        if (bssid != "" && bssid != "BSSID") {
            print bssid "|" channel "|" privacy "|" power "|" beacons "|" ivs "|" essid
        }
    }
    ' "$csv_file" | sort -t'|' -k2 -n > "$parsed_aps"

    # Parse Clients section
    log "Parsing client data..."
    awk '
    BEGIN { FS=","; in_client=0 }
    /^Station MAC/ { in_client=1; next }
    in_client && /^[0-9A-Fa-f]/ {
        mac=$1; power=$4; packets=$5; bssid=$6; probed=$7
        gsub(/^[ \t]+|[ \t]+$/, "", mac)
        gsub(/^[ \t]+|[ \t]+$/, "", power)
        gsub(/^[ \t]+|[ \t]+$/, "", packets)
        gsub(/^[ \t]+|[ \t]+$/, "", bssid)
        gsub(/^[ \t]+|[ \t]+$/, "", probed)
        if (mac != "") {
            print mac "|" power "|" packets "|" bssid "|" probed
        }
    }
    ' "$csv_file" > "$parsed_clients"

    local ap_count client_count
    ap_count=$(wc -l < "$parsed_aps")
    client_count=$(wc -l < "$parsed_clients")
    log "Parsed: $ap_count APs, $client_count clients"

    log "✓ Data parsing complete"
}

#=============================================================================
# Phase 6: Report Generation
#=============================================================================
generate_report() {
    section "PHASE 6: REPORT GENERATION"

    local parsed_aps="${RAW_DIR}/parsed_aps.csv"
    local parsed_clients="${RAW_DIR}/parsed_clients.csv"
    local oui_output="${RAW_DIR}/oui_lookups.csv"
    local probes_file="${RAW_DIR}/probe_requests.txt"
    local date_str
    date_str=$(date +%Y-%m-%d)
    local time_str
    time_str=$(date +%H:%M:%S)

    log "Generating report at: $REPORT_FILE"

    # Build OUI lookup associative array for the report
    declare -A OUI_MAP
    if [[ -f "$oui_output" ]]; then
        while IFS=',' read -r mac vendor; do
            OUI_MAP["$mac"]="$vendor"
        done < "$oui_output"
    fi

    # Helper: look up OUI for a MAC
    lookup_oui() {
        local mac="${1^^}"
        echo "${OUI_MAP[$mac]:-UNKNOWN}"
    }

    # ---- Begin Report ----
    cat > "$REPORT_FILE" <<HEADER
# Wireless Reconnaissance Report

**Date:** ${date_str}
**Time:** ${time_str}
**Operator:** Thon (Venom/Agent)
**Authority:** Eddie (Sovereign/Principal)
**Classification:** RECON ONLY — No offensive operations conducted
**Equipment:** WiFi Pineapple Mark 7, MT7601U monitor radio (${PINE_MON_IF})
**Scan Duration:** ${SCAN_DURATION}s channel-hop + ${CHANNEL_DWELL}s × 3 targeted channels
**Band:** ${PINE_BAND}

---

## Executive Summary

HEADER

    # Count APs and clients
    local ap_count=0 client_count=0
    [[ -f "$parsed_aps" ]] && ap_count=$(wc -l < "$parsed_aps")
    [[ -f "$parsed_clients" ]] && client_count=$(wc -l < "$parsed_clients")

    # Count deny list entries
    local deny_mac_count=0 deny_ssid_count=0
    [[ -f "${RAW_DIR}/denylist_macs.txt" ]] && deny_mac_count=$(wc -l < "${RAW_DIR}/denylist_macs.txt")
    [[ -f "${RAW_DIR}/denylist_ssids.txt" ]] && deny_ssid_count=$(wc -l < "${RAW_DIR}/denylist_ssids.txt")

    cat >> "$REPORT_FILE" <<SUMMARY
Passive wireless reconnaissance discovered **${ap_count} access points** and **${client_count} client stations**. Home network protection configured with **${deny_mac_count} MAC** and **${deny_ssid_count} SSID** deny list entries.

---

## Home Network Protection

### Deny List (MAC Filter — Blacklist Mode)
SUMMARY

    if [[ -f "${RAW_DIR}/denylist_macs.txt" ]]; then
        echo '```' >> "$REPORT_FILE"
        while IFS= read -r mac; do
            local vendor
            vendor=$(lookup_oui "$mac")
            echo "${mac}  (${vendor})" >> "$REPORT_FILE"
        done < "${RAW_DIR}/denylist_macs.txt"
        echo '```' >> "$REPORT_FILE"
    fi

    if [[ -f "${RAW_DIR}/denylist_ssids.txt" ]]; then
        echo "" >> "$REPORT_FILE"
        echo "### SSID Deny List" >> "$REPORT_FILE"
        echo '```' >> "$REPORT_FILE"
        cat "${RAW_DIR}/denylist_ssids.txt" >> "$REPORT_FILE"
        echo '```' >> "$REPORT_FILE"
    fi

    # ---- AP Inventory ----
    cat >> "$REPORT_FILE" <<'AP_HEADER'

---

## Access Point Inventory

| BSSID | Channel | ESSID | Security | Power (dBm) | Beacons | IVs | Vendor |
|---|---|---|---|---|---|---|---|
AP_HEADER

    if [[ -f "$parsed_aps" ]]; then
        while IFS='|' read -r bssid channel privacy power beacons ivs essid; do
            local vendor
            vendor=$(lookup_oui "$bssid")
            [[ -z "$essid" || "$essid" =~ ^[[:space:]]*$ ]] && essid="*(hidden)*"
            echo "| ${bssid} | ${channel} | ${essid} | ${privacy} | ${power} | ${beacons} | ${ivs} | ${vendor} |" >> "$REPORT_FILE"
        done < "$parsed_aps"
    fi

    # ---- Channel Summary ----
    echo "" >> "$REPORT_FILE"
    echo "### Channel Distribution" >> "$REPORT_FILE"
    echo '```' >> "$REPORT_FILE"
    if [[ -f "$parsed_aps" ]]; then
        awk -F'|' '{
            ch=$2; gsub(/^[ \t]+|[ \t]+$/, "", ch)
            count[ch]++
        }
        END {
            for (ch in count) printf "Channel %2s: %d APs\n", ch, count[ch]
        }' "$parsed_aps" | sort -t' ' -k2 -n >> "$REPORT_FILE"
    fi
    echo '```' >> "$REPORT_FILE"

    # ---- Client Inventory ----
    cat >> "$REPORT_FILE" <<'CLIENT_HEADER'

---

## Client Station Inventory

| Client MAC | Vendor | Associated BSSID | Power (dBm) | Packets | Probed SSIDs |
|---|---|---|---|---|---|
CLIENT_HEADER

    if [[ -f "$parsed_clients" ]]; then
        while IFS='|' read -r mac power packets bssid probed; do
            local vendor
            vendor=$(lookup_oui "$mac")
            [[ -z "$bssid" || "$bssid" == "(not associated)" ]] && bssid="*(not associated)*"
            [[ -z "$probed" || "$probed" =~ ^[[:space:]]*$ ]] && probed="—"
            echo "| ${mac} | ${vendor} | ${bssid} | ${power} | ${packets} | ${probed} |" >> "$REPORT_FILE"
        done < "$parsed_clients"
    fi

    # ---- Probe Requests ----
    echo "" >> "$REPORT_FILE"
    echo "---" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "## Probe Request Analysis" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"

    if [[ -f "$probes_file" ]] && [[ -s "$probes_file" ]]; then
        echo "| Client MAC | Vendor | Probing For |" >> "$REPORT_FILE"
        echo "|---|---|---|" >> "$REPORT_FILE"

        # Extract unique device+SSID pairs from probe requests
        grep -oiE 'SA:([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}' "$probes_file" 2>/dev/null | \
            sed 's/^SA://i' | sort -u | while read -r mac; do
                local vendor probed_ssids
                vendor=$(lookup_oui "$mac")
                probed_ssids=$(grep -i "$mac" "$probes_file" | \
                               grep -oP 'Probe Request \(\K[^)]+' 2>/dev/null | \
                               sort -u | tr '\n' ', ' | sed 's/,$//' || echo "broadcast")
                [[ -z "$probed_ssids" ]] && probed_ssids="*(broadcast)*"
                echo "| ${mac} | ${vendor} | ${probed_ssids} |" >> "$REPORT_FILE"
            done
    else
        echo "No probe requests captured during this scan." >> "$REPORT_FILE"
    fi

    # ---- Signal Strength Map ----
    echo "" >> "$REPORT_FILE"
    echo "---" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "## Signal Strength Map" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo '```' >> "$REPORT_FILE"
    echo "Signal Legend: ████ Excellent (<-50)  ███ Good (-50 to -65)  ██ Fair (-65 to -80)  █ Weak (>-80)" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"

    if [[ -f "$parsed_aps" ]]; then
        while IFS='|' read -r bssid channel privacy power beacons ivs essid; do
            local db_val="${power// /}"
            [[ -z "$essid" || "$essid" =~ ^[[:space:]]*$ ]] && essid="(hidden)"
            # Build signal bar
            local bar=""
            local abs_power=${db_val#-}
            if [[ "$abs_power" -lt 50 ]]; then
                bar="████████████"
            elif [[ "$abs_power" -lt 60 ]]; then
                bar="████████"
            elif [[ "$abs_power" -lt 65 ]]; then
                bar="███████"
            elif [[ "$abs_power" -lt 70 ]]; then
                bar="██████"
            elif [[ "$abs_power" -lt 75 ]]; then
                bar="█████"
            elif [[ "$abs_power" -lt 80 ]]; then
                bar="████"
            elif [[ "$abs_power" -lt 85 ]]; then
                bar="███"
            else
                bar="██"
            fi
            printf "  %-25s %s  %s dBm\n" "$essid" "$bar" "$db_val" >> "$REPORT_FILE"
        done < <(sort -t'|' -k4 -n "$parsed_aps")
    fi

    echo '```' >> "$REPORT_FILE"

    # ---- Methodology ----
    cat >> "$REPORT_FILE" <<'METHODOLOGY'

---

## Methodology & Reproduction

### Quick Reproduction

```bash
# From Kali container (or any host with sshpass + sqlite3):
./pineapple_recon.sh --scan-duration 90 --verbose

# Skip deny list if already configured:
./pineapple_recon.sh --skip-denylist --scan-duration 120

# From Windows host:
powershell -File E:\Thon\scripts\run_recon.ps1
```

### Manual Steps

1. **Enumerate home devices**: `Get-NetNeighbor -AddressFamily IPv4` (Windows)
2. **Push deny list**: SCP filters.db → sqlite3 INSERT → SCP back → `killall -HUP pineapple`
3. **Passive scan**: `airodump-ng wlan1mon --write /tmp/recon --output-format csv --band bg`
4. **Probe capture**: `tcpdump -i wlan1mon -e | grep 'Probe Request'`
5. **OUI lookup**: `python3 -c "import json; oui=json.load(open('/etc/pineapple/ouis')); ..."`

### Requirements
- WiFi Pineapple Mark 7 (FW 2.1.3+) at 172.16.42.1
- Monitor interface: wlan1mon
- Kali container with: sshpass, sqlite3
- SSH credentials configured
METHODOLOGY

    # ---- Footer ----
    cat >> "$REPORT_FILE" <<FOOTER

---

*Report generated automatically by pineapple_recon.sh at ${date_str} ${time_str}*
*Raw data preserved in: ${RAW_DIR}*
FOOTER

    log "✓ Report written to: $REPORT_FILE"
    log "  Raw data in: $RAW_DIR"
}

#=============================================================================
# Main Execution
#=============================================================================
main() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║     PINEAPPLE WIRELESS RECONNAISSANCE — AUTOMATED SCAN     ║"
    echo "║     Classification: RECON ONLY                             ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    log "Configuration:"
    log "  Pineapple: ${PINE_IP} (${PINE_MON_IF})"
    log "  Scan duration: ${SCAN_DURATION}s"
    log "  Band: ${PINE_BAND}"
    log "  Home SSIDs: ${HOME_SSIDS}"
    log "  Report dir: ${REPORT_DIR}"
    echo ""

    local start_time
    start_time=$(date +%s)

    preflight
    enumerate_home_devices
    push_denylist
    active_ap_scan
    wireless_scan
    capture_probes
    oui_lookup
    parse_airodump
    generate_report

    local end_time elapsed
    end_time=$(date +%s)
    elapsed=$((end_time - start_time))

    section "COMPLETE"
    log "Total runtime: ${elapsed}s"
    log "Report: $REPORT_FILE"
    log "Raw data: $RAW_DIR"
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║  RECON COMPLETE — All data saved. No offensive actions.     ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
}

main "$@"
