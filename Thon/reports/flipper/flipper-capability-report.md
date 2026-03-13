# Flipper Zero — Full-Spectrum Capability Report

> Generated: 2026-03-11T04:04:23.769241+00:00
> Firmware: Official 1.4.3
> Device: Alaudisu (HW rev 12)

## Device Identity Card

| Field | Value |
|-------|-------|
| Model | Flipper Zero |
| Name | Alaudisu |
| UID | `272BEF0027E18000` |
| HW Rev | 12 |
| Target | 7 |
| Region | CA |
| FW Version | 1.4.3 |
| FW Origin | Official |
| FW Build | 05-12-2025 |
| API | 87.1 |
| Git Hash | `8622f1a2` |
| BLE MAC | `272BEF27E180` |
| Battery | 100% (charged) |
| Battery Health | 100% |

## C2 Transport Assessment

| Transport | Status | Notes |
|-----------|--------|-------|
| USB Serial | ✅ Confirmed | COM4, 115200 baud, full CLI access |
| WiFi | ❌ Not viable | ESP32-S2 devboard with Marauder firmware — no native CLI relay over WiFi |
| Bluetooth | ❓ Unknown | BLE serial profile support depends on firmware — needs runtime probe |

## Command Tree

### `[32mbt` (2 commands)

| Command | Description | Latency |
|---------|-------------|---------|
| `[32mbt 2mbt` |  | 4036ms |
| `[32mbt [31mcould` | not find command `2mbt`, try `help`[0m | 4031ms |

### `!` (60 commands)

| Command | Description | Latency |
|---------|-------------|---------|
| `! device_info_major` | 2 | 4040ms |
| `! device_info_minor` | 4 | 4032ms |
| `! hardware_model` | Flipper Zero | 4036ms |
| `! hardware_uid` | 272BEF0027E18000 | 4039ms |
| `! hardware_otp_ver` | 2 | 4033ms |
| `! hardware_timestamp` | 1684850676 | 4036ms |
| `! hardware_ver` | 12 | 4025ms |
| `! hardware_target` | 7 | 4023ms |
| `! hardware_body` | 9 | 4040ms |
| `! hardware_connect` | 6 | 4037ms |
| `! hardware_display` | 2 | 4039ms |
| `! hardware_color` | 2 | 4033ms |
| `! hardware_region` | 4 | 4034ms |
| `! hardware_region_provisioned` | CA | 4021ms |
| `! hardware_name` | Alaudisu | 4022ms |
| `! firmware_commit` | 8622f1a2 | 4040ms |
| `! firmware_commit_dirty` | false | 4036ms |
| `! firmware_branch` | 1.4.3 | 4024ms |
| `! firmware_branch_num` | 0 | 4022ms |
| `! firmware_version` | 1.4.3 | 4030ms |
| `! firmware_build_date` | 05-12-2025 | 4024ms |
| `! firmware_target` | 7 | 4033ms |
| `! firmware_api_major` | 87 | 4029ms |
| `! firmware_api_minor` | 1 | 4024ms |
| `! firmware_origin_fork` | Official | 4027ms |
| `! firmware_origin_git` | https://github.com/flipperdevices/flipperzero-firmware | 4037ms |
| `! radio_alive` | true | 4024ms |
| `! radio_mode` | Stack | 4034ms |
| `! radio_fus_major` | 1 | 4025ms |
| `! radio_fus_minor` | 2 | 4039ms |
| `! radio_fus_sub` | 0 | 4040ms |
| `! radio_fus_sram2b` | 16K | 4036ms |
| `! radio_fus_sram2a` | 0K | 4029ms |
| `! radio_fus_flash` | 24K | 4030ms |
| `! radio_stack_type` | 3 | 4028ms |
| `! radio_stack_major` | 1 | 4039ms |
| `! radio_stack_minor` | 20 | 4030ms |
| `! radio_stack_sub` | 0 | 4037ms |
| `! radio_stack_branch` | 0 | 4037ms |
| `! radio_stack_release` | 2 | 4027ms |
| `! radio_stack_sram2b` | 19K | 4027ms |
| `! radio_stack_sram2a` | 14K | 4034ms |
| `! radio_stack_sram1` | 0K | 4034ms |
| `! radio_stack_flash` | 116K | 4021ms |
| `! radio_ble_mac` | 272BEF27E180 | 4036ms |
| `! enclave_valid_keys` | 10 | 4021ms |
| `! enclave_valid` | true | 4039ms |
| `! system_debug` | 0 | 4025ms |
| `! system_lock` | 0 | 4024ms |
| `! system_orient` | 0 | 4040ms |
| `! system_sleep_legacy` | 0 | 4040ms |
| `! system_stealth` | 0 | 4032ms |
| `! system_heap_track` | 0 | 4028ms |
| `! system_boot` | 0 | 4025ms |
| `! system_locale_time` | 0 | 4030ms |
| `! system_locale_date` | 0 | 4038ms |
| `! system_locale_unit` | 0 | 4040ms |
| `! system_log_level` | 0 | 4029ms |
| `! protobuf_version_major` | 0 | 4029ms |
| `! protobuf_version_minor` | 25 | 4038ms |

### `Available` (1 commands)

| Command | Description | Latency |
|---------|-------------|---------|
| `Available [31mcould` | not find command `Available`, try `help`[0m | 4023ms |

### `Find` (1 commands)

| Command | Description | Latency |
|---------|-------------|---------|
| `Find [31mcould` | not find command `Find`, try `help`[0m | 4031ms |

### `If` (1 commands)

| Command | Description | Latency |
|---------|-------------|---------|
| `If [31mcould` | not find command `If`, try `help`[0m | 4029ms |

### `badusb` (1 commands)

| Command | Description | Latency |
|---------|-------------|---------|
| `badusb [31mcould` | not find command `badusb`, try `help`[0m | 4030ms |

### `bt` (1 commands)

| Command | Description | Latency |
|---------|-------------|---------|
| `bt [31mthis` | command cannot be run while an application is open[0m | 4030ms |

### `buzzer` (1 commands)

| Command | Description | Latency |
|---------|-------------|---------|
| `buzzer [31mthis` | command cannot be run while an application is open[0m | 4021ms |

### `crypto` (1 commands)

| Command | Description | Latency |
|---------|-------------|---------|
| `crypto [31mthis` | command cannot be run while an application is open[0m | 4026ms |

### `debug` (1 commands)

| Command | Description | Latency |
|---------|-------------|---------|
| `debug [31mcould` | not find command `debug`, try `help`[0m | 4024ms |

### `desktop` (1 commands)

| Command | Description | Latency |
|---------|-------------|---------|
| `desktop [31mcould` | not find command `desktop`, try `help`[0m | 4027ms |

### `device_info` (60 commands)

| Command | Description | Latency |
|---------|-------------|---------|
| `device_info device_info_major` | 2 | 4023ms |
| `device_info device_info_minor` | 4 | 4040ms |
| `device_info hardware_model` | Flipper Zero | 4025ms |
| `device_info hardware_uid` | 272BEF0027E18000 | 4027ms |
| `device_info hardware_otp_ver` | 2 | 4033ms |
| `device_info hardware_timestamp` | 1684850676 | 4029ms |
| `device_info hardware_ver` | 12 | 4029ms |
| `device_info hardware_target` | 7 | 4031ms |
| `device_info hardware_body` | 9 | 4029ms |
| `device_info hardware_connect` | 6 | 4031ms |
| `device_info hardware_display` | 2 | 4025ms |
| `device_info hardware_color` | 2 | 4032ms |
| `device_info hardware_region` | 4 | 4040ms |
| `device_info hardware_region_provisioned` | CA | 4027ms |
| `device_info hardware_name` | Alaudisu | 4024ms |
| `device_info firmware_commit` | 8622f1a2 | 4038ms |
| `device_info firmware_commit_dirty` | false | 4031ms |
| `device_info firmware_branch` | 1.4.3 | 4025ms |
| `device_info firmware_branch_num` | 0 | 4029ms |
| `device_info firmware_version` | 1.4.3 | 4030ms |
| `device_info firmware_build_date` | 05-12-2025 | 4024ms |
| `device_info firmware_target` | 7 | 4026ms |
| `device_info firmware_api_major` | 87 | 4030ms |
| `device_info firmware_api_minor` | 1 | 4036ms |
| `device_info firmware_origin_fork` | Official | 4034ms |
| `device_info firmware_origin_git` | https://github.com/flipperdevices/flipperzero-firmware | 4027ms |
| `device_info radio_alive` | true | 4021ms |
| `device_info radio_mode` | Stack | 4029ms |
| `device_info radio_fus_major` | 1 | 4034ms |
| `device_info radio_fus_minor` | 2 | 4007ms |
| `device_info radio_fus_sub` | 0 | 4027ms |
| `device_info radio_fus_sram2b` | 16K | 4030ms |
| `device_info radio_fus_sram2a` | 0K | 4037ms |
| `device_info radio_fus_flash` | 24K | 4022ms |
| `device_info radio_stack_type` | 3 | 4027ms |
| `device_info radio_stack_major` | 1 | 4038ms |
| `device_info radio_stack_minor` | 20 | 4024ms |
| `device_info radio_stack_sub` | 0 | 4032ms |
| `device_info radio_stack_branch` | 0 | 4026ms |
| `device_info radio_stack_release` | 2 | 4027ms |
| `device_info radio_stack_sram2b` | 19K | 4029ms |
| `device_info radio_stack_sram2a` | 14K | 4028ms |
| `device_info radio_stack_sram1` | 0K | 4024ms |
| `device_info radio_stack_flash` | 116K | 4035ms |
| `device_info radio_ble_mac` | 272BEF27E180 | 4030ms |
| `device_info enclave_valid_keys` | 10 | 4034ms |
| `device_info enclave_valid` | true | 4021ms |
| `device_info system_debug` | 0 | 4026ms |
| `device_info system_lock` | 0 | 4026ms |
| `device_info system_orient` | 0 | 4031ms |
| `device_info system_sleep_legacy` | 0 | 4024ms |
| `device_info system_stealth` | 0 | 4023ms |
| `device_info system_heap_track` | 0 | 4030ms |
| `device_info system_boot` | 0 | 4027ms |
| `device_info system_locale_time` | 0 | 4025ms |
| `device_info system_locale_date` | 0 | 4029ms |
| `device_info system_locale_unit` | 0 | 4028ms |
| `device_info system_log_level` | 0 | 4028ms |
| `device_info protobuf_version_major` | 0 | 4027ms |
| `device_info protobuf_version_minor` | 25 | 4022ms |

**Total commands discovered: 131**

## Capability Matrix Summary

| Risk Level | Count | Definition |
|------------|-------|------------|
| none | 127 | Read-only, no state change, no RF emission |
| low | 0 | Reversible config change, no RF emission |
| medium | 0 | RF emission, LED/vibro actuation, reversible |
| high | 0 | Active wireless attacks, persistent config changes |
| critical | 4 | Firmware mod, factory reset, bootloader ops |

**MCP tool candidates: 127 / 131**

## MCP Server Architecture Recommendations

1. **Framework:** Python FastMCP (consistency with Thon MCP ecosystem)
2. **Transport:** USB serial primary via pyserial, WiFi fallback pending ESP firmware change
3. **Connection:** Singleton serial session with heartbeat (`power info` every 60s)
4. **Tool grouping:** By subsystem (subghz, nfc, rfid, storage, etc.)
5. **Risk gating:** Embed risk_level in tool metadata; Medium+ requires operator confirm
6. **Streaming:** Sub-GHz RX, NFC detect as async generators with teardown hooks
7. **State tracking:** Track active subsystem sessions, enforce single-active-stream
8. **Error handling:** Parse Flipper error patterns, retry on serial timeout, abort on disconnect
