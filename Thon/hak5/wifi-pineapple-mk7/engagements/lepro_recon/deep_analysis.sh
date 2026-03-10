#!/bin/bash
echo "=== All broadcast data frames by source ==="
tshark -r /tmp/tuya_pairing3.pcap -Y "wlan.da==ff:ff:ff:ff:ff:ff && wlan.fc.type==2" -T fields -e wlan.sa -e frame.len 2>/dev/null | sort | uniq -c | sort -rn | head -20

echo ""
echo "=== All unique source MACs sending data frames ==="
tshark -r /tmp/tuya_pairing3.pcap -Y "wlan.fc.type==2" -T fields -e wlan.sa 2>/dev/null | sort -u

echo ""
echo "=== Looking for new MACs (potential bulb) ==="
tshark -r /tmp/tuya_pairing3.pcap -Y "wlan.fc.type==0 && wlan.fc.subtype==0" -T fields -e wlan.sa -e wlan.da -e wlan.ssid 2>/dev/null | head -20

echo ""
echo "=== Probe requests (bulb searching for network) ==="
tshark -r /tmp/tuya_pairing3.pcap -Y "wlan.fc.type==0 && wlan.fc.subtype==4" -T fields -e wlan.sa -e wlan.ssid 2>/dev/null | sort -u | head -20

echo ""
echo "=== Authentication frames ==="
tshark -r /tmp/tuya_pairing3.pcap -Y "wlan.fc.type==0 && wlan.fc.subtype==11" -T fields -e wlan.sa -e wlan.da 2>/dev/null | head -20

echo ""
echo "=== Association requests ==="
tshark -r /tmp/tuya_pairing3.pcap -Y "wlan.fc.type==0 && wlan.fc.subtype==0" -T fields -e wlan.sa -e wlan.da 2>/dev/null | head -20

echo ""
echo "=== Frames from known bulb MAC 70:89:76 OUI ==="
tshark -r /tmp/tuya_pairing3.pcap -Y "wlan.sa[0:3]==70:89:76 || wlan.da[0:3]==70:89:76" -T fields -e frame.number -e wlan.sa -e wlan.da -e wlan.fc.type_subtype -e frame.len 2>/dev/null | head -30

echo ""
echo "DONE"
