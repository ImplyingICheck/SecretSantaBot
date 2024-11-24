#!/usr/bin/env ash

# Start vault
vault server -config "$VAULT_CONFIG" &
sleep 3
[ ! -e generated_keys.txt ] && vault operator init > generated_keys.txt

sleep 3
# Parse unsealed keys
keys="$(awk -F': ' '/Unseal Key [0-9]+:/ {print $2}' generated_keys.txt)"
for key in $keys; do
    vault operator unseal "$key"
done

# Get root token
rootToken="$(awk -F': ' '/Initial Root Token:/ {print $2}' generated_keys.txt)"
[ ! -e /secrets/root_token.txt ] && echo "$rootToken" > "$ROOT_TOKEN_FILE"

# Enable kv secrets
vault login "$rootToken"
vault secrets enable -path=secret kv

wait
