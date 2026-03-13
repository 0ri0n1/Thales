# Antigravity IDE WSL `run_command` Failure: Shell Integration `-c` Flag Mismatch

**Date:** 2026-03-10
**Operator:** Thon (Venom)
**Authority:** Eddie (Sovereign)
**Platform:** Antigravity IDE v1.20.5 (Google VS Code fork, codename Jetski)
**Classification:** Diagnostic / Configuration Remediation

---

## Problem Statement

Eddie reported the Antigravity IDE agent's `run_command` function was not working with WSL. Commands either hung indefinitely or failed immediately. Goal: achieve parity with Cursor IDE, where WSL command execution works reliably.

## Environment

- **OS:** Windows 10 (build 26200)
- **WSL2 Distros:** Ubuntu-22.04 (running), kali-linux, ParrotOS, archlinux (stopped), docker-desktop (running)
- **Antigravity:** v1.107.0, installed at `C:\Users\Dallas\AppData\Local\Programs\Antigravity`
- **Antigravity config:** `C:\Users\Dallas\AppData\Roaming\Antigravity\User\settings.json`
- **Cursor config:** `C:\Users\Dallas\AppData\Roaming\Cursor\User\settings.json`

## Architecture Context

Antigravity's agent uses a tool called `run_in_terminal` (internally registered as tool ID `run_in_terminal`, reference name `nYn`). Unlike Cursor's Shell tool which spawns a separate child process and writes temp `.ps1` scripts, Antigravity's tool operates through the **integrated terminal widget** and depends on **VS Code shell integration** to detect command start, completion, and exit codes.

Shell integration works by injecting monitoring scripts into the shell session. On startup, the terminal process launcher appends arguments to the shell executable — specifically, it passes `-c <integration_script>` to initialize the integration hooks.

## Diagnostic Chain

### Phase 1: Initial Assessment

1. Confirmed WSL functional from Cursor — `wsl bash -c 'echo test'` works fine
2. Located Antigravity installation and extension structure
3. Found `antigravity-code-executor` extension — simple VM sandbox for JS, not the command tool
4. Found `run_in_terminal` tool definition in `workbench.desktop.main.js` (line ~7316)
5. Confirmed the tool creates persistent terminal sessions via `getCopilotProfile()` and monitors via shell integration

### Phase 2: Settings Comparison

**Cursor settings (working for manual terminals, agent uses separate mechanism):**
```json
"terminal.integrated.profiles.windows": {
    "Ubuntu-22.04 (WSL)": {
        "path": "C:\\Windows\\System32\\wsl.exe",
        "args": ["-d", "Ubuntu-22.04"],
        "icon": "terminal-bash"
    }
},
"terminal.integrated.defaultProfile.windows": "Ubuntu-22.04 (WSL)"
```

**Antigravity original settings (from `Antigravity.old`):**
```json
// No terminal profile overrides — auto-detection
```

### Phase 3: Failed Approaches

| Attempt | Configuration | Result |
|---------|--------------|--------|
| Match Cursor exactly | `wsl.exe` + `["-d", "Ubuntu-22.04"]` | `Invalid command line argument: -c` — every command fails |
| Add `--exec bash` | `wsl.exe` + `["-d", "Ubuntu-22.04", "--exec", "bash"]` | Same `-c` error — shell integration injects `-c` at `wsl.exe` level |
| Switch to PowerShell default | `PowerShell` as default profile | Commands run, but agent generates bash syntax (`&&`) which PowerShell 5.x rejects |
| Remove `--exec bash`, keep `wsl.exe` | `wsl.exe` + `["-d", "Ubuntu-22.04"]` | Same `-c` error |

### Phase 4: Root Cause Discovery

The `-c` flag is a **bash argument**, not a `wsl.exe` argument. Shell integration injects `-c <script>` as an argument to whatever executable is specified in the profile's `path` field. 

- `wsl.exe -c <script>` → **Fails** — `wsl.exe` does not accept `-c`
- `bash.exe -c <script>` → **Works** — `bash.exe` is a POSIX-compliant shell

Critical discovery: `C:\Windows\System32\bash.exe` exists on the system. This is **not Git Bash** — it is Microsoft's WSL bash wrapper. It launches bash inside the default WSL distro and natively accepts `-c`.

```
C:\Windows\System32\bash.exe -c "echo test"     → Works (runs in Ubuntu-22.04)
C:\Windows\System32\wsl.exe -c "echo test"      → Fails (invalid argument)
C:\Windows\System32\wsl.exe -d Ubuntu-22.04 -- bash -c "echo test" → Works (but not how profiles invoke)
```

### Phase 5: Resolution

Changed profile path from `wsl.exe` to `bash.exe`:

```json
"terminal.integrated.profiles.windows": {
    "Ubuntu-22.04 (WSL)": {
        "path": "C:\\Windows\\System32\\bash.exe",
        "icon": "terminal-bash"
    }
},
"terminal.integrated.defaultProfile.windows": "Ubuntu-22.04 (WSL)"
```

**Result:** Agent commands execute successfully through WSL2 Ubuntu-22.04 with full shell integration.

## Why Cursor Works Differently

Cursor's agent (Shell tool) does **not** use the integrated terminal. It:
1. Writes a temp `.ps1` script to `C:\Users\Dallas\AppData\Local\Temp\ps-script-*.ps1`
2. Executes it as a child process
3. Reads stdout/stderr directly

This bypasses shell integration entirely. Cursor's WSL profile setting (`wsl.exe`) only affects manual terminal tabs, not agent command execution. This is why identical settings produce different behavior between the two IDEs.

## Key Distinction

| Executable | Type | Accepts `-c` | Connects to WSL | Shell Integration Compatible |
|-----------|------|-------------|-----------------|------------------------------|
| `C:\Windows\System32\wsl.exe` | WSL launcher | No | Yes | No |
| `C:\Windows\System32\bash.exe` | WSL bash wrapper | Yes | Yes (default distro) | Yes |
| `C:\Program Files\Git\bin\bash.exe` | Git Bash (MinGW) | Yes | No (local MinGW) | Yes |

## Previous Hangs Explained

Eddie reported intermittent hangs when the old config (no overrides) was in use. With no profile overrides, Antigravity auto-detects shells and likely selected `bash.exe` from PATH. Shell integration would load, but WSL startup latency occasionally exceeded the shell integration timeout, causing the tool to hang waiting for the integration handshake. This is tunable via `terminal.integrated.shellIntegration.timeout` if it recurs.

## Final Configuration

```json
{
  "window.commandCenter": true,
  "terminal.integrated.enableMultiLinePasteWarning": "never",
  "geminicodeassist.project": "tactical-snowfall-bzsgc",
  "php.suggest.basic": false,
  "php.validate.enable": false,
  "emmet.excludeLanguages": ["markdown", "php"],
  "workbench.colorTheme": "Visual Studio Dark",
  "json.schemaDownload.enable": true,
  "terminal.integrated.profiles.windows": {
    "Ubuntu-22.04 (WSL)": {
      "path": "C:\\Windows\\System32\\bash.exe",
      "icon": "terminal-bash"
    }
  },
  "terminal.integrated.defaultProfile.windows": "Ubuntu-22.04 (WSL)",
  "markdown.preview.breaks": true
}
```

## Lessons Learned

1. **Same settings ≠ same behavior** across VS Code forks. The agent execution mechanism matters more than the terminal profile config.
2. **`wsl.exe` and `bash.exe` are not interchangeable** as shell profile paths. `wsl.exe` is a launcher; `bash.exe` is a POSIX shell wrapper. Only the latter is compatible with VS Code shell integration injection.
3. **Auto-detection was already close to correct.** The old Antigravity config with no overrides likely worked because auto-detection picked `bash.exe`. Explicit configuration with `wsl.exe` broke it.
4. **Cursor's architecture is fundamentally different** — its agent spawns child processes, not terminal widgets. Matching Cursor's settings.json is necessary but not sufficient for Antigravity parity.
