#!/bin/sh
# ============================================================================
# PAYLOAD: recon.sh — Network Reconnaissance
# DEVICE:  LAN Turtle (Hak5) — OpenWrt / BusyBox ash
# PURPOSE: Host discovery and service enumeration from implant position
# TOOLS:   nmap, arp, ip
# OPSEC:   Output to /tmp only. Excludes C2 overlay (10.8.0.0/24, VPN).
#          Excludes management subnet (172.16.84.0/24).
# ============================================================================

# --- Configuration -----------------------------------------------------------
OUTDIR="/tmp/recon"
IFACE="eth1"                          # Target-facing interface
EXCLUDE_NETS="10.8.0.0/24,172.16.84.0/24"  # VPN overlay + management
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG="${OUTDIR}/recon_${TIMESTAMP}.log"

# --- Functions ---------------------------------------------------------------
usage() {
    echo "Usage: $0 <discover|enumerate|full> [target_cidr]"
    echo ""
    echo "Modes:"
    echo "  discover   - ARP + ping sweep, host discovery only"
    echo "  enumerate  - Service scan on discovered or specified hosts"
    echo "  full       - Discovery then enumeration (default target net)"
    echo ""
    echo "Examples:"
    echo "  $0 discover                    # Discover hosts on eth1 subnet"
    echo "  $0 enumerate 192.168.1.1-10    # Enumerate specific range"
    echo "  $0 full 192.168.1.0/24         # Full recon of subnet"
    exit 1
}

log() {
    echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG"
}

cleanup() {
    log "Recon complete. Output: ${OUTDIR}"
    ls -la "$OUTDIR" >> "$LOG" 2>&1
}

get_target_net() {
    # Derive target subnet from eth1 DHCP address
    _ip=$(ip -4 addr show "$IFACE" 2>/dev/null | grep -o 'inet [0-9.]*' | awk '{print $2}')
    if [ -z "$_ip" ]; then
        echo ""
        return 1
    fi
    # Assume /24 for discovery
    echo "${_ip%.*}.0/24"
}

# --- Main --------------------------------------------------------------------
trap cleanup EXIT

MODE="${1:-full}"
TARGET="${2:-}"

mkdir -p "$OUTDIR"

# Auto-detect target network if not specified
if [ -z "$TARGET" ]; then
    TARGET=$(get_target_net)
    if [ -z "$TARGET" ]; then
        log "ERROR: Cannot determine target network from ${IFACE}. Specify manually."
        exit 1
    fi
fi

log "=== LAN Turtle Recon ==="
log "Mode: ${MODE}"
log "Target: ${TARGET}"
log "Interface: ${IFACE}"
log "Exclusions: ${EXCLUDE_NETS}"

case "$MODE" in
    discover)
        log "--- Phase 1: Host Discovery ---"

        # ARP table dump (passive, instant)
        log "ARP table snapshot:"
        ip neigh show dev "$IFACE" 2>/dev/null | tee -a "$LOG"

        # Ping sweep (fast, low noise)
        log "Ping sweep: ${TARGET}"
        nmap -sn -n --exclude "$EXCLUDE_NETS" -oG "${OUTDIR}/hosts_${TIMESTAMP}.gnmap" \
             "$TARGET" 2>/dev/null | grep "Host:" | tee -a "$LOG"
        ;;

    enumerate)
        log "--- Service Enumeration ---"
        log "Target: ${TARGET}"

        # Top 100 ports, version detection, fast timing
        nmap -sV -sC --top-ports 100 -T3 -n \
             --exclude "$EXCLUDE_NETS" \
             -oN "${OUTDIR}/services_${TIMESTAMP}.nmap" \
             -oG "${OUTDIR}/services_${TIMESTAMP}.gnmap" \
             "$TARGET" 2>/dev/null | tee -a "$LOG"
        ;;

    full)
        log "--- Phase 1: Host Discovery ---"

        # ARP snapshot
        ip neigh show dev "$IFACE" 2>/dev/null > "${OUTDIR}/arp_${TIMESTAMP}.txt"
        log "ARP entries: $(wc -l < "${OUTDIR}/arp_${TIMESTAMP}.txt")"

        # Ping sweep
        log "Ping sweep: ${TARGET}"
        nmap -sn -n --exclude "$EXCLUDE_NETS" -oG "${OUTDIR}/hosts_${TIMESTAMP}.gnmap" \
             "$TARGET" 2>/dev/null

        LIVE=$(grep "Status: Up" "${OUTDIR}/hosts_${TIMESTAMP}.gnmap" 2>/dev/null | \
               grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')
        HOSTCOUNT=$(echo "$LIVE" | grep -c .)
        log "Live hosts: ${HOSTCOUNT}"

        if [ "$HOSTCOUNT" -eq 0 ]; then
            log "No live hosts found. Exiting."
            exit 0
        fi

        # Phase 2: Enumerate live hosts
        log "--- Phase 2: Service Enumeration ---"
        echo "$LIVE" > "${OUTDIR}/live_hosts.txt"

        nmap -sV --top-ports 100 -T3 -n \
             --exclude "$EXCLUDE_NETS" \
             -oN "${OUTDIR}/services_${TIMESTAMP}.nmap" \
             -oG "${OUTDIR}/services_${TIMESTAMP}.gnmap" \
             -iL "${OUTDIR}/live_hosts.txt" 2>/dev/null | tee -a "$LOG"
        ;;

    *)
        usage
        ;;
esac

log "=== Recon Complete ==="
