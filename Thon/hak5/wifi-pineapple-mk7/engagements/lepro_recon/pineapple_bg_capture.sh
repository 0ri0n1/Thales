#!/bin/sh
tcpdump -i wlan2 -w /tmp/phone_bulb.pcap host 192.168.1.78 and host 192.168.1.82 -c 5000 &
echo $!
