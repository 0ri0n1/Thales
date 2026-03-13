#!/bin/bash
export TERM=xterm
export COLUMNS=120
export LINES=40
setsid bash /home/dallas/data/overnight_crack.sh </dev/null >/home/dallas/data/crack_stdout.txt 2>&1 &
BGPID=$!
sleep 3
echo "Launched PID: $BGPID"
ps aux | grep -E 'hashcat|overnight' | grep -v grep
echo "---"
head -10 /home/dallas/data/crack_log.txt 2>/dev/null
