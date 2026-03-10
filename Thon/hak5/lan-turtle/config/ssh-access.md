# LAN Turtle SSH Access Configuration

## Credentials

- **User**: root
- **Password**: sh3llz (default, unchanged)
- **Key auth**: ED25519 key (`thon@kali-turtle`)

## Key Locations

| Location | Path |
|----------|------|
| Private key (WSL kali) | /root/.ssh/id_ed25519_turtle |
| Public key (WSL kali) | /root/.ssh/id_ed25519_turtle.pub |
| Authorized keys (turtle) | /root/.ssh/authorized_keys |
| SSH config entry (WSL kali) | /root/.ssh/config → Host turtle |

## SSH Config (WSL kali-linux)

```
Host turtle
    HostName 172.16.84.1
    User root
    IdentityFile /root/.ssh/id_ed25519_turtle
    StrictHostKeyChecking no
```

## Quick Access

```bash
# From WSL kali-linux:
ssh turtle

# From any SSH client:
ssh -i /root/.ssh/id_ed25519_turtle root@172.16.84.1
```

## SSH Fingerprints (post-reflash)

Host keys regenerated on 2026-03-08 after firmware recovery.
Key types: ECDSA, ED25519, RSA.

## Notes

- Turtle runs OpenSSH sshd (NOT Dropbear despite being OpenWrt)
- First-boot wizard runs on initial SSH login (ncurses TUI)
- Enter `turtle` at ash prompt to launch TUI management shell
- Authorized keys go in `/root/.ssh/authorized_keys` (standard OpenSSH path)
