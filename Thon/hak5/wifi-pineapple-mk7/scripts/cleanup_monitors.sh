#!/bin/sh
# Remove all monitor mode interfaces and restore clean state

# Remove wlan1mon explicitly
iw wlan1mon del 2>/dev/null
echo "wlan1mon: removed"

# Check for any remaining monitor interfaces
for iface in $(iw dev 2>/dev/null | grep "Interface" | awk '{print $2}'); do
    TYPE=$(iw dev "$iface" info 2>/dev/null | grep "type" | awk '{print $2}')
    if [ "$TYPE" = "monitor" ]; then
        echo "Removing monitor: $iface"
        iw "$iface" del 2>/dev/null
    fi
done

# Restore wlan1 to managed if it exists
if iw dev wlan1 info >/dev/null 2>&1; then
    ip link set wlan1 down 2>/dev/null
    iw wlan1 set type managed 2>/dev/null
    ip link set wlan1 up 2>/dev/null
    echo "wlan1: restored to managed"
fi

sleep 1

echo ""
echo "=== Final Interface State ==="
iw dev
echo ""
MONITORS=$(iw dev 2>/dev/null | grep -c "type monitor")
echo "Monitor interfaces remaining: $MONITORS"
