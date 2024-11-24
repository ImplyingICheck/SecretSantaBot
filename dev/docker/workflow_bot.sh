#!/usr/bin/env ash

VAULT_TOKEN="$(cat $ROOT_TOKEN_FILE)" && \
export VAULT_TOKEN && \
python "secret_santa_bot/main.py"
