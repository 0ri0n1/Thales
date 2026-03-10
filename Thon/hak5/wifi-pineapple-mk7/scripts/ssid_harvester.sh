#!/bin/sh
# ============================================================================
# SSID HARVESTER — Passive SSID/Name Collection
# ============================================================================
# Operation:   Passive SSID harvesting from beacons, probes, and PineAP logs
# Platform:    WiFi Pineapple Mark 7 (OpenWrt / ash)
# Authority:   Eddie (Sovereign) / Operator: Thon (Venom)
# Mode:        PASSIVE ONLY — no deauth, no association, no injection
#
# Collects SSIDs from three sources:
#   1. PineAP probe log (client probe requests)
#   2. iwinfo wlan2 scan (beacon survey)
#   3. airodump-ng CSV (monitor mode passive capture)
#
# Output: /tmp/ssid_harvest/  (timestamped, deduplicated)
# ============================================================================

HARVEST_DIR="/tmp/ssid_harvest"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOGFILE="${HARVEST_DIR}/harvest_${TIMESTAMP}.log"
SSID_MASTER="${HARVEST_DIR}/ssid_master.txt"
SSID_NEW="${HARVEST_DIR}/ssid_new_${TIMESTAMP}.txt"
PROBE_LOG="${HARVEST_DIR}/probes_${TIMESTAMP}.txt"
BEACON_LOG="${HARVEST_DIR}/beacons_${TIMESTAMP}.txt"
AIRODUMP_PREFIX="${HARVEST_DIR}/airodump_${TIMESTAMP}"
DURATION=${1:-300}  # Default 5 minutes, override with $1

# --- Setup ---
mkdir -p "$HARVEST_DIR"
touch "$SSID_MASTER"

log() {
    echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOGFILE"
}

log "=== SSID HARVESTER STARTED ==="
log "Duration: ${DURATION}s"
log "Output: ${HARVEST_DIR}"
log "Mode: PASSIVE COLLECTION ONLY"

# --- Source 1: PineAP Probe Log ---
log "[SRC1] Pulling PineAP probe request log..."
if [ -f /tmp/pineap.log ]; then
    # PineAP logs probe requests as: SSID\tMAC\tTimestamp
    cat /tmp/pineap.log | awk -F'\t' '{print $1}' | sort -u > "$PROBE_LOG" 2>/dev/null
    PROBE_COUNT=$(wc -l < "$PROBE_LOG" 2>/dev/null || echo 0)
    log "[SRC1] Extracted ${PROBE_COUNT} unique SSIDs from PineAP probes"
else
    log "[SRC1] No PineAP probe log found at /tmp/pineap.log"
    touch "$PROBE_LOG"
fi

# --- Source 2: iwinfo Beacon Survey ---
log "[SRC2] Running iwinfo wlan2 scan (beacon survey)..."
iwinfo wlan2 scan 2>/dev/null | grep 'ESSID:' | sed 's/.*ESSID: "\(.*\)"/\1/' | grep -v '^$' | sort -u > "$BEACON_LOG" 2>/dev/null
BEACON_COUNT=$(wc -l < "$BEACON_LOG" 2>/dev/null || echo 0)
log "[SRC2] Captured ${BEACON_COUNT} unique SSIDs from beacons"

# --- Source 3: airodump-ng Passive Capture ---
log "[SRC3] Checking for monitor interface wlan1mon..."
if iwconfig wlan1mon >/dev/null 2>&1; then
    log "[SRC3] Starting airodump-ng passive capture for ${DURATION}s..."
    # Run in background, channel cycling, 2.4GHz band
    airodump-ng wlan1mon --band bg -w "$AIRODUMP_PREFIX" --output-format csv --write-interval 30 >/dev/null 2>&1 &
    AIRO_PID=$!
    log "[SRC3] airodump-ng running as PID ${AIRO_PID}"

    # Wait for capture duration
    sleep "$DURATION"

    # Kill airodump
    kill "$AIRO_PID" 2>/dev/null
    wait "$AIRO_PID" 2>/dev/null
    log "[SRC3] airodump-ng capture complete"

    # Parse CSV for SSIDs (field 14 in airodump CSV = ESSID)
    AIRO_CSV="${AIRODUMP_PREFIX}-01.csv"
    if [ -f "$AIRO_CSV" ]; then
        # APs section: ESSID is the last field (field 14)
        awk -F',' '/^[0-9A-Fa-f]{2}:/{
            gsub(/^ +| +$/, "", $14);
            if ($14 != "" && $14 != " ") print $14
        }' "$AIRO_CSV" | sort -u >> "$BEACON_LOG"

        # Stations section: Probed ESSIDs are field 7+
        awk -F',' '/Station MAC/{found=1; next} found{
            for(i=7;i<=NF;i++){
                gsub(/^ +| +$/, "", $i);
                if ($i != "" && $i != " ") print $i
            }
        }' "$AIRO_CSV" >> "$PROBE_LOG"

        AIRO_AP_COUNT=$(awk -F',' '/^[0-9A-Fa-f]{2}:/{gsub(/^ +| +$/, "", $14); if ($14 != "") print $14}' "$AIRO_CSV" | sort -u | wc -l)
        log "[SRC3] Parsed ${AIRO_AP_COUNT} SSIDs from airodump CSV"
    else
        log "[SRC3] WARNING: No CSV output from airodump-ng"
    fi
else
    log "[SRC3] SKIP: wlan1mon not available (monitor mode not active)"
    log "[SRC3] To enable: airmon-ng start wlan1"
fi

# --- Deduplication & Master List ---
log "[MERGE] Deduplicating and merging into master list..."

# Combine all sources, deduplicate
cat "$PROBE_LOG" "$BEACON_LOG" 2>/dev/null | sort -u | grep -v '^$' > "${HARVEST_DIR}/.tmp_all_ssids"

# Find new SSIDs not in master
comm -23 "${HARVEST_DIR}/.tmp_all_ssids" "$SSID_MASTER" > "$SSID_NEW" 2>/dev/null

NEW_COUNT=$(wc -l < "$SSID_NEW" 2>/dev/null || echo 0)
TOTAL_THIS_RUN=$(wc -l < "${HARVEST_DIR}/.tmp_all_ssids" 2>/dev/null || echo 0)

# Append new SSIDs to master
if [ -s "$SSID_NEW" ]; then
    cat "$SSID_NEW" >> "$SSID_MASTER"
    sort -u "$SSID_MASTER" -o "$SSID_MASTER"
fi

MASTER_TOTAL=$(wc -l < "$SSID_MASTER" 2>/dev/null || echo 0)

# Cleanup temp
rm -f "${HARVEST_DIR}/.tmp_all_ssids"

# --- Report ---
log "========================================="
log "  HARVEST COMPLETE"
log "========================================="
log "  This run:     ${TOTAL_THIS_RUN} SSIDs seen"
log "  New SSIDs:    ${NEW_COUNT}"
log "  Master total: ${MASTER_TOTAL} unique SSIDs"
log "========================================="

if [ -s "$SSID_NEW" ]; then
    log "  NEW SSIDs this run:"
    while read -r ssid; do
        log "    + ${ssid}"
    done < "$SSID_NEW"
fi

log "=== SSID HARVESTER FINISHED ==="
