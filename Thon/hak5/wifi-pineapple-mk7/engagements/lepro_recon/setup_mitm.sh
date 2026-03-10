#!/bin/bash

echo "=== Check mitmproxy availability ==="
which mitmproxy 2>/dev/null
which mitmweb 2>/dev/null
which mitmdump 2>/dev/null
dpkg -l 2>/dev/null | grep mitmproxy

echo ""
echo "=== Check for arpspoof/ettercap ==="
which arpspoof 2>/dev/null
which ettercap 2>/dev/null
which bettercap 2>/dev/null

echo ""
echo "=== Check Pineapple for tcpdump capabilities ==="
echo "We can capture phone-to-cloud HTTPS traffic on the Pineapple"
echo "Phone IP: 192.168.1.78"
echo "Gateway: 192.168.1.254"
echo ""
echo "Strategy: ARP spoof the phone so traffic routes through Pineapple"
echo "Then use mitmproxy/sslstrip to intercept HTTPS"
echo ""
echo "Alternatively: Set up transparent proxy on Kali container"

echo ""
echo "=== Alternative: DNS redirect approach ==="
echo "If we can redirect a1.tuyaus.com to our proxy, we intercept the API calls"
echo "The local_key appears in GET device info responses"

echo ""
echo "DONE"
