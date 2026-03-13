# Flipper Zero — Device Profile

> **Status:** ✅ COMPLETE — Full serial interrogation successful  
> **Last updated:** 2026-03-10T19:58Z  

---

## USB Identity

| Field | Value |
|-------|-------|
| **VID:PID** | `0483:5740` (STMicroelectronics — CDC Serial) |
| **Serial Number** | `FLIP_ALAUDISU` |
| **COM Port** | COM4 |
| **Host OS** | Windows 11 / DESKTOP-9IHNBQC |

---

## Firmware

| Field | Value |
|-------|-------|
| **Version** | **1.4.3** |
| **Branch** | `1.4.3` |
| **Commit** | `8622f1a2` (clean) |
| **Build Date** | 2025-12-05 |
| **Target** | 7 |
| **API** | 87.1 |
| **Origin** | **Official** (flipperdevices/flipperzero-firmware) |
| **Protobuf** | 0.25 |

## Hardware

| Field | Value |
|-------|-------|
| **Model** | Flipper Zero |
| **UID** | `272BEF0027E18000` |
| **OTP Version** | 2 |
| **Hardware Rev** | 12 |
| **Target** | 7 |
| **Body** | 9 |
| **Connect** | 6 |
| **Display** | 2 |
| **Color** | 2 |
| **Region (builtin)** | 4 |
| **Region (provisioned)** | 🇨🇦 CA |
| **Device Name** | Alaudisu |

## Radio (BLE/Bluetooth)

| Field | Value |
|-------|-------|
| **Status** | ✅ Alive |
| **Mode** | Stack |
| **FUS Version** | 1.2.0 |
| **Stack Version** | 1.20.0.0.2 |
| **BLE MAC** | `27:2B:EF:27:E1:80` |
| **HCI Version** | 13 (BT 5.4) |
| **Manufacturer** | 48 (STMicro) |

## Power / Battery

| Field | Value |
|-------|-------|
| **Charge Level** | 59% |
| **State** | Charging |
| **Voltage** | 3.855V |
| **Current** | 840mA |
| **Temperature** | 27°C |
| **Battery Health** | 100% |
| **Capacity (remaining)** | 1239 mAh |
| **Capacity (full)** | 2100 mAh |
| **Capacity (design)** | 2100 mAh |

## Storage

### SD Card (External)
| Field | Value |
|-------|-------|
| **Label** | FLIPPER |
| **Type** | FAT32 |
| **Total** | 15,169,536 KiB (~14.5 GB) |
| **Free** | 15,136,256 KiB (~14.4 GB) |
| **Card** | Samsung 02TM SA16G v5.5 |
| **SN** | `309d177c` (02/2019) |

### Internal
| Field | Value |
|-------|-------|
| **Label** | Alaudisu |
| **Type** | Virtual |
| **Total** | 15,169,536 KiB |
| **Free** | 15,136,624 KiB |

## Security

| Field | Value |
|-------|-------|
| **Enclave Valid** | ✅ true |
| **Valid Keys** | 10 |
| **Debug** | Disabled (0) |
| **Lock** | Disabled (0) |
| **Stealth** | Disabled (0) |

---

## WiFi Devboard v1

| Field | Value |
|-------|-------|
| **Chipset** | ESP32-S2 (expected) |
| **Detected as USB device** | ❌ Not separately enumerated |
| **Connection** | Via Flipper GPIO header |
| **Firmware** | TBD — requires GPIO passthrough test |
| **Status** | Physically attached; needs `wifi_marauder` app or GPIO serial passthrough to query |

---

## Other Devices on USB Bus

| VID:PID | Name | Notes |
|---------|------|-------|
| `1532:0D06` | Razer Stream Controller (COM3) | |
| `1532:00AB` | Razer Basilisk V3 Pro | Mouse |
| `0BDA:2838` | RTL-SDR | SDR dongle |
| `0BDA:A811` | Realtek RTL8811AU | WiFi adapter |
