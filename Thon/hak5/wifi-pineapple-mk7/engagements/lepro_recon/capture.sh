#!/bin/sh
tcpdump -i wlan2 -w /tmp/lepro_capture.pcap host 192.168.1.82 -c 100000 &
TCPDUMP_PID=$!
echo "tcpdump started with PID: $TCPDUMP_PID"
sleep 300
kill $TCPDUMP_PID 2>/dev/null
echo "Capture complete after 5 minutes"
ls -la /tmp/lepro_capture.pcap
