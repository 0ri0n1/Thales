#!/bin/bash
echo "=== Trying ed25519 ==="
ssh -v -o StrictHostKeyChecking=no -o ConnectTimeout=5 -o IdentitiesOnly=yes -i /root/.ssh/id_ed25519 root@172.16.42.1 'echo AUTH_OK_ED' 2>/tmp/ssh_debug_ed.log
echo "EXIT: $?"
echo ""
echo "=== Trying RSA ==="
ssh -v -o StrictHostKeyChecking=no -o ConnectTimeout=5 -o IdentitiesOnly=yes -i /root/.ssh/id_rsa root@172.16.42.1 'echo AUTH_OK_RSA' 2>/tmp/ssh_debug_rsa.log
echo "EXIT: $?"
echo ""
echo "=== ED25519 Debug Log ==="
cat /tmp/ssh_debug_ed.log
echo ""
echo "=== RSA Debug Log ==="
cat /tmp/ssh_debug_rsa.log
