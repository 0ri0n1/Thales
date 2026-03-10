#!/bin/sh
# ============================================================================
# PAYLOAD: arp-watch.sh — Passive Network Mapping
# DEVICE:  LAN Turtle (Hak5) — OpenWrt / BusyBox ash
# PURPOSE: Monitor ARP table for new hosts appearing on target network.
#          Builds network map over time without generating traffic.
# TOOLS:   ip, arp (BusyBox built-in)
# OPSEC:   100% passive — reads kernel ARP cache only. Zero network noise.
#          Output to /tmp only. Minimal CPU/RAM footprint.
# ============================================================================

# --- Configuration -----------------------------------------------------------
OUTDIR="/tmp/arp-watch"
IFACE="eth1"                          # Target-facing interface
POLL_INTERVAL=30                       # Seconds between ARP table checks
KNOWN_FILE="${OUTDIR}/known_hosts.txt"
LOG="${OUTDIR}/arp-watch.log"
PIDFILE="/tmp/arp-watch.pid"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# --- Functions ---------------------------------------------------------------
usage() {
    echo "Usage: $0 <start|stop|status|snapshot> [interval]"
    echo ""
    echo "Modes:"
    echo "  start [seconds]  - Begin passive ARP monitoring (default: ${POLL_INTERVAL}s)"
    echo "  stop             - Stop monitoring"
    echo "  status           - Show known hosts and monitor state"
    echo "  snapshot         - One-time ARP table dump"
    exit 1
}

log() {
    echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG"
}

get_arp_entries() {
    # Get ARP entries for target interface, exclude incomplete
    ip neigh show dev "$IFACE" 2>/dev/null | \
        grep -v "FAILED" | \
        awk '{print $1, $3, $5}' | \
        sort
}

snapshot() {
    mkdir -p "$OUTDIR"
    _file="${OUTDIR}/snapshot_${TIMESTAMP}.txt"
    log "=== ARP Snapshot ==="
    echo "# ARP Snapshot $(date)" > "$_file"
    echo "# IP MAC STATE" >> "$_file"
    get_arp_entries | tee -a "$_file" "$LOG"
    _count=$(wc -l < "$_file")
    log "Entries: $(( _count - 2 ))"
}

monitor_loop() {
    mkdir -p "$OUTDIR"
    touch "$KNOWN_FILE"

    log "=== ARP Watch Started ==="
    log "Interface: ${IFACE}"
    log "Poll interval: ${POLL_INTERVAL}s"
    log "Known hosts file: ${KNOWN_FILE}"

    while true; do
        get_arp_entries | while IFS= read -r _entry; do
            _ip=$(echo "$_entry" | awk '{print $1}')
            _mac=$(echo "$_entry" | awk '{print $2}')

            # Check if this IP+MAC combo is already known
            if ! grep -q "^${_ip} ${_mac}" "$KNOWN_FILE" 2>/dev/null; then
                _ts=$(date '+%Y-%m-%d %H:%M:%S')
                echo "${_ip} ${_mac} ${_ts}" >> "$KNOWN_FILE"
                log "NEW HOST: ${_ip} (${_mac})"
            fi
        done

        sleep "$POLL_INTERVAL"
    done
}

start_watch() {
    if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
        log "Already running (PID $(cat "$PIDFILE"))"
        return 1
    fi

    monitor_loop &
    echo $! > "$PIDFILE"
    log "ARP watch started in background (PID $!)"
}

stop_watch() {
    if [ -f "$PIDFILE" ]; then
        _pid=$(cat "$PIDFILE")
        if kill -0 "$_pid" 2>/dev/null; then
            kill "$_pid"
            # Also kill any child sleep processes
            pkill -P "$_pid" 2>/dev/null
            log "ARP watch stopped (PID ${_pid})"
        else
            log "Process ${_pid} not running"
        fi
        rm -f "$PIDFILE"
    else
        log "No PID file found"
    fi
}

show_status() {
    echo "=== ARP Watch Status ==="
    if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
        echo "State: RUNNING (PID $(cat "$PIDFILE"))"
    else
        echo "State: STOPPED"
    fi
    echo ""

    if [ -f "$KNOWN_FILE" ]; then
        _count=$(wc -l < "$KNOWN_FILE")
        echo "Known hosts: ${_count}"
        echo ""
        echo "IP              MAC                First Seen"
        echo "------          ---                ----------"
        cat "$KNOWN_FILE"
    else
        echo "Known hosts: 0"
    fi
    echo ""
    echo "Current ARP table (${IFACE}):"
    get_arp_entries
}

# --- Main --------------------------------------------------------------------
case "${1:-}" in
    start)
        [ -n "$2" ] && POLL_INTERVAL="$2"
        start_watch
        ;;
    stop)
        stop_watch
        ;;
    status)
        show_status
        ;;
    snapshot)
        snapshot
        ;;
    *)
        usage
        ;;
esac
