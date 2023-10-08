"""Sets enviornment variables for secret_santa_bot. Notably, reading the token
used by the bot."""
import os
import pathlib
import subprocess
import sys

import hvac
import hvac.exceptions

_APPLICATION_NAME = 'SecretSantaBot'
_TOKEN_USERNAME = 'token'


class Vault(hvac.Client):
    def __init__(self, url: str, token: str, **kwargs):
        super().__init__(url=url, token=token, **kwargs)
        self.vault = self.secrets.kv.v2

    def read_secret_token(self,
        service_name: str = _APPLICATION_NAME, username: str = _TOKEN_USERNAME
    ) -> str | None:
        try:
            return self.vault.read_secret(path=service_name)['data']['data'][username]
        except hvac.exceptions.InvalidPath:
            return self.prompt_user_for_token_sync()

    def prompt_user_for_token_sync(self):
        token = input(f'No {_TOKEN_USERNAME} found for {_APPLICATION_NAME}.\nEnter an API token: ')
        self.vault.create_or_update_secret(path=_APPLICATION_NAME, secret={_TOKEN_USERNAME: token})
        return token

def _get_secret_santa_bot_path():
    file_depth = 1
    root_directory = pathlib.Path(__file__).parents[file_depth]
    secret_santa_bot_script = root_directory.joinpath(
        'secret_santa_bot', 'santa.py'
    )
    return secret_santa_bot_script

if __name__ == '__main__':
    vault = Vault(url='http://localhost:8200',
    token=os.environ['VAULT_TOKEN'])
    script_path = _get_secret_santa_bot_path()
    discord_authentication_token = vault.read_secret_token()
    subprocess.run([sys.executable, script_path, discord_authentication_token])
