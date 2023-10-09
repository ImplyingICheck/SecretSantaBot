from typing import Any

import hvac
from hvac.api import secrets_engines


class Vault(hvac.Client):
    _APPLICATION_NAME = 'SecretSantaBot'
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
        try:
            return self.vault.read_secret(path=service_name)['data']['data'][
                username
            ]
        except (hvac.exceptions.InvalidPath, KeyError):
            return self.prompt_user_for_token(
                service_name=service_name, username=username
            )

    def prompt_user_for_token(
        self,
        service_name,
        username,
    ) -> str:
        token = input(
            f'No {username} found for {service_name}.\n'
            f'Enter a new {username}: '
        )
        token = token.strip()
        self.vault.create_or_update_secret(
            path=service_name, secret={username: token}
        )
        return token
