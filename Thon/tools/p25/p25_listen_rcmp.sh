#!/bin/bash
# ============================================================
#  P25 RCMP Listener — Docker Kali
#  Connects to rtl_tcp server on Windows, decodes P25
# ============================================================
#
#  PREREQUISITE: start_rtl_tcp_server.bat must be running on Windows
#
#  Usage from Docker Kali:
#    bash /root/data/p25_listen_rcmp.sh [frequency_mhz]
#
#  Examples:
#    bash /root/data/p25_listen_rcmp.sh          # Default: 155.475 MHz (RCMP AB VHF)
#    bash /root/data/p25_listen_rcmp.sh 155.370  # RCMP Mutual Aid
#    bash /root/data/p25_listen_rcmp.sh 154.280  # Fire Mutual Aid
# ============================================================

FREQ_MHZ="${1:-155.475}"
FREQ_HZ=$(echo "$FREQ_MHZ * 1000000" | bc | cut -d. -f1)
HOST="host.docker.internal"
PORT="1234"
SAMPLE_RATE=48000
GAIN=40
OUTPUT_DIR="/root/data/p25_audio"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$OUTPUT_DIR"

echo ""
echo "  P25 RCMP Listener"
echo "  ================="
echo "  Frequency: ${FREQ_MHZ} MHz ($FREQ_HZ Hz)"
echo "  RTL-TCP:   ${HOST}:${PORT}"
echo "  Sample Rate: ${SAMPLE_RATE} Hz"
echo "  Output: ${OUTPUT_DIR}/p25_${FREQ_MHZ}MHz_${TIMESTAMP}.raw"
echo ""
echo "  NOTE: If you hear digital buzzing instead of voice, the"
echo "  channel may be encrypted. Try a different frequency."
echo ""
echo "  Ctrl+C to stop."
echo ""

# Method 1: Try rtl_fm with rtl_tcp remote syntax
# (works if librtlsdr was built with rtl_tcp client support)
echo "[*] Attempting rtl_fm connection to rtl_tcp server..."
rtl_fm -d "rtl_tcp:${HOST}:${PORT}" \
    -f "$FREQ_HZ" \
    -M fm \
    -s "$SAMPLE_RATE" \
    -g "$GAIN" \
    -l 20 \
    -E dc \
    - 2>/dev/null | \
    tee "${OUTPUT_DIR}/p25_${FREQ_MHZ}MHz_${TIMESTAMP}.raw" | \
    dsdccx -i - -o "${OUTPUT_DIR}/p25_decoded_${FREQ_MHZ}MHz_${TIMESTAMP}.raw" -v 1

EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "[!] rtl_fm with rtl_tcp syntax failed (exit code: $EXIT_CODE)"
    echo "[!] Your Docker rtl_fm may not support remote rtl_tcp connections."
    echo ""
    echo "  FALLBACK OPTIONS:"
    echo "  1. Use the Windows batch file: p25_capture_windows.bat"
    echo "     (Records raw FM audio, then decode offline in Docker)"
    echo "  2. Use the WSL pipe: p25_listen_wsl.sh"
    echo "     (Pipes Windows rtl_fm.exe directly to WSL dsdccx)"
    echo ""
fi
