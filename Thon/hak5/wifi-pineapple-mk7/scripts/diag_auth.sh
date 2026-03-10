#!/bin/bash
# Auth diagnostic: check which keys the Pineapple will accept
echo "=== SSH Auth Debug ==="
ssh -vvv -o StrictHostKeyChecking=no -o ConnectTimeout=5 -o IdentitiesOnly=yes -i /root/.ssh/id_ed25519 root@172.16.42.1 'echo AUTH_OK' 2>&1 | grep -iE '(offer|auth|try|next|denied|accept|pubkey|method|identit)'
echo ""
echo "=== Return code: $? ==="
echo ""
echo "=== Trying RSA key ==="
ssh -vvv -o StrictHostKeyChecking=no -o ConnectTimeout=5 -o IdentitiesOnly=yes -i /root/.ssh/id_rsa root@172.16.42.1 'echo AUTH_OK_RSA' 2>&1 | grep -iE '(offer|auth|try|next|denied|accept|pubkey|method|identit)'
echo ""
echo "=== RSA Return code: $? ==="
