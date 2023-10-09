"""Sets enviornment variables for secret_santa_bot. Notably, reading the token
used by the bot."""
import os
import pathlib
from typing import Any

import hvac
import hvac.exceptions
from hvac.api import secrets_engines

import secret_santa_bot.bot.santa

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
        except hvac.exceptions.InvalidPath:
            return self.prompt_user_for_token_sync()

    def prompt_user_for_token_sync(self) -> str:
        token = input(
            f'No {self._TOKEN_USERNAME} found for {self._APPLICATION_NAME}.\n'
            f'Enter an API token: '
        )
        token = token.strip()
        self.vault.create_or_update_secret(
            path=self._APPLICATION_NAME, secret={self._TOKEN_USERNAME: token}
        )
        return token


def _get_secret_santa_bot_path() -> pathlib.Path:
    file_depth = 1
    root_directory = pathlib.Path(__file__).parents[file_depth]
    secret_santa_bot_script = root_directory.joinpath(
        'secret_santa_bot', 'santa.py'
    )
    return secret_santa_bot_script


if __name__ == '__main__':
    vault: Vault = Vault(
        url='http://vault:8200', token=os.environ['VAULT_TOKEN']
    )
    script_path: pathlib.Path = _get_secret_santa_bot_path()
    discord_authentication_token: str = vault.read_secret_token()
    secret_santa_bot.bot.santa.main(discord_authentication_token)
