"""Helper class to access secrets stored in "Hashicorp vault"."""
from typing import Any, NotRequired, TypedDict

import hvac
from hvac.api import secrets_engines
from hvac import exceptions as hvac_exceptions


class TokenRequest(TypedDict):
    """Type hint for parameters of prompt_user_token."""

    service_name: str
    username: str
    secret_data: NotRequired[dict[str, str]]


class Vault(hvac.Client):
    """Provides helper functions for accessing secrets stored in "Hashicorp
    vault"."""

    _APPLICATION_NAME = 'secretsantabot'
    _TOKEN_USERNAME = 'token'

    def __init__(self, url: str, token: str, **kwargs: Any):
        super().__init__(url=url, token=token, **kwargs)
        # hvac.Client.secrets.kv.v2 is type magic done by hvac for referencing
        # secrets_engines.KvV2
        self.vault: secrets_engines.KvV2 = self.secrets.kv.v2  # type: ignore

    def read_secret_token(
        self,
        service_name: str = _APPLICATION_NAME,
        username: str = _TOKEN_USERNAME,
    ) -> str:
        """Reads a secret token from the Vault. If not present, prompts the
        caller for a token, then creates it under that *username*."""
        try:
            secret = self.vault.read_secret(path=service_name)['data']['data']
        except hvac_exceptions.InvalidPath:
            request_if_error: TokenRequest = {
                'service_name': service_name,
                'username': username,
            }
        else:
            try:
                return secret[username]
            except KeyError:
                request_if_error: TokenRequest = {
                    'service_name': service_name,
                    'username': username,
                    'secret_data': secret,
                }
        return self.prompt_user_for_token(**request_if_error)

    def prompt_user_for_token(
        self,
        service_name: str,
        username: str,
        secret_data: dict[str, Any] | None = None,
    ) -> str:
        token = input(
            f'No {username} found for {service_name}.\n'
            f'Enter a new {username}: '
        )
        token = token.strip()
        new_secret = {username: token}
        if secret_data:
            secret_data.update(new_secret)
        else:
            secret_data = new_secret
        self.vault.create_or_update_secret(
            path=service_name, secret=secret_data
        )
        return self.read_secret_token(service_name, username)
