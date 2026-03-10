#!/bin/bash
PASS="Mousepad7"
HOST="172.16.42.1"

PUBKEY="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIA0N5YLGv+XjZXvB+J+Jka7oUv9PwagwwFxhtyIpwyvT root@docker-desktop"

echo "=== Adding Kali container SSH key to Pineapple ==="
sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@$HOST "mkdir -p /root/.ssh && chmod 700 /root/.ssh && echo '$PUBKEY' >> /root/.ssh/authorized_keys && sort -u /root/.ssh/authorized_keys -o /root/.ssh/authorized_keys && chmod 600 /root/.ssh/authorized_keys && echo 'Done. Keys:' && cat /root/.ssh/authorized_keys"

echo "Exit: $?"
