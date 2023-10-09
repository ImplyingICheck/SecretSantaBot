from typing import Any

import hvac
from hvac.api import secrets_engines


class Vault(hvac.Client):
    _APPLICATION_NAME = 'secretsantabot'
    _TOKEN_USERNAME = 'token'

    def __init__(self, url: str, token: str, **kwargs: Any):
        super().__init__(url=url, token=token, **kwargs)
        # hvac.Client.secrets.kv.v2 is type magic done by hvac for reference secrets_engines.KvV2
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
        except hvac.exceptions.InvalidPath:
            request_if_error = {'service_name': service_name, 'username': username}
        else:
            try:
                return secret[username]
            except KeyError:
                request_if_error = {'service_name': service_name, 'username': username, 'secret_data': secret}
        return self.prompt_user_for_token(**request_if_error)

    def prompt_user_for_token(
        self, service_name: str, username: str, secret_data: dict[str, Any] | None = None
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
