"""Sets enviornment variables for secret_santa_bot. Notably, reading the token
used by the bot."""
import os
import pathlib

import secret_santa_bot.bot.santa
from secret_santa_bot import _vault


def _get_secret_santa_bot_path() -> pathlib.Path:
    file_depth = 1
    root_directory = pathlib.Path(__file__).parents[file_depth]
    secret_santa_bot_script = root_directory.joinpath(
        'secret_santa_bot', 'santa.py'
    )
    return secret_santa_bot_script


if __name__ == '__main__':
    vault: _vault.Vault = _vault.Vault(
        url='http://localhost:8200', token=os.environ['VAULT_TOKEN']
    )
    os.environ['GUILD_ID'] = vault.read_secret_token(username='GUILD_ID')
    script_path: pathlib.Path = _get_secret_santa_bot_path()
    discord_authentication_token: str = vault.read_secret_token()
    secret_santa_bot.bot.santa.main(discord_authentication_token)
