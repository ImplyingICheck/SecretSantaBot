#!/usr/bin/env ash

VAULT_TOKEN="$(cat /runtime_secrets/root_token.txt)" && \
export VAULT_TOKEN && \
python secret_santa_bot/main.py
