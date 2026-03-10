#!/bin/bash
PASS="Mousepad7"
HOST="172.16.42.1"
PUBKEY=$(cat /root/.ssh/id_ed25519.pub)

echo "=== Re-provisioning SSH key on Pineapple ==="
sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@$HOST bash <<REMOTECMD
mkdir -p /root/.ssh
chmod 700 /root/.ssh
touch /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys

if grep -q "$(echo '$PUBKEY' | awk '{print \$2}')" /root/.ssh/authorized_keys 2>/dev/null; then
    echo "Key already present."
else
    echo '$PUBKEY' >> /root/.ssh/authorized_keys
    echo "Key added."
fi

echo ""
echo "authorized_keys contents:"
cat /root/.ssh/authorized_keys
echo ""
echo "=== SSH KEY FIX DONE ==="
REMOTECMD

echo "SSH exit: $?"
