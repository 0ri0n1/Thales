# Flipper Zero WiFi Module — Recommendations

> **Date:** 2026-03-10  
> **Status:** Passive advisory — no actions taken without approval  

---

## 1. CRITICAL: Install WiFi Marauder Companion App

**Priority: BLOCKING**

The WiFi devboard (ESP32-S2) is physically attached, but the **[ESP32] WiFi Marauder companion app** is not installed on the Flipper's SD card. Without it, there is no way to command the WiFi devboard from the Flipper.

**Currently installed GPIO apps:** `gpio.fap`, `air_mouse.fap`, `vgm_air_mouse.fap` — none are WiFi-related.

### Installation (pick one):
1. **Via Flipper Mobile App** — Open the Flipper app on your phone → Apps → GPIO → search "WiFi Marauder" → Install
2. **Via qFlipper** — Open qFlipper → Apps → GPIO → WiFi Marauder → Install
3. **Manual** — Download `esp32_wifi_marauder.fap` from the [Flipper Apps Catalog](https://lab.flipper.net/apps/esp32_wifi_marauder) → copy to `/ext/apps/GPIO/`

> [!IMPORTANT]
> The WiFi devboard itself also needs **Marauder firmware** flashed onto the ESP32-S2 chip for full functionality. If it's running stock firmware, the Marauder app will be unable to communicate. Flashing Marauder onto the devboard requires `esptool` (already installed) and is a **staged operation requiring approval**.

---

## 2. WiFi Devboard Firmware

### Current: Unknown (cannot query until Marauder app is installed)

### Recommended: ESP32 Marauder

| Factor | Recommendation |
|--------|---------------|
| **Best firmware** | [ESP32 Marauder](https://github.com/justcallmekoko/ESP32Marauder) |
| **Why** | Full offensive WiFi suite: scanning, deauth, PMKID, evil portal, pcap |
| **Stock AT alternative** | Only if you need basic WiFi client connectivity |
| **Blackmagic** | Only if you need SWD/JTAG hardware debugging |

### Flash Marauder (if needed, staged operation)
```bash
python -m esptool --chip esp32s2 --port COMx \
  --baud 921600 write_flash 0x1000 marauder_esp32s2.bin
```

---

## 3. Firmware Upgrade Notes

| Component | Current | Status |
|-----------|---------|--------|
| Flipper Zero FW | **1.4.3** (Official, 2025-12-05) | ✅ Up to date (just updated via qFlipper) |
| WiFi Devboard FW | Unknown | ⚠️ Needs Marauder app to query |
| BLE Stack | 1.20.0 | ✅ Current |

## 4. Suggested Next Steps

| # | Action | Risk | Approval |
|---|--------|------|----------|
| 1 | **Install WiFi Marauder companion app** on Flipper | None | No |
| 2 | Query WiFi devboard firmware via Marauder app | None | No |
| 3 | Flash Marauder onto ESP32-S2 (if not already installed) | Low — reversible | **Yes** |
| 4 | Run first WiFi AP scan as proof-of-life | None | No |
| 5 | Explore pcap capture workflow | None | No |

## 5. Hardware Synergies

Your USB bus already has complementary RF tools:
- **Flipper + Marauder** — 2.4 GHz WiFi field scans, offensive tools
- **RTL8811AU** (already connected) — 5 GHz dual-band monitoring
- **RTL-SDR** (already connected) — Wide RF spectrum analysis
