"""Sets enviornment variables for secret_santa_bot. Notably, reading the token
used by the bot."""
import os

from secret_santa_bot import _vault


def main():
    vault: _vault.Vault = _vault.Vault(
        url=os.environ['VAULT_PATH'], token=os.environ['VAULT_TOKEN']
    )
    os.environ['GUILD_ID'] = vault.read_secret_token(username='guild_id')
    # In-line import as discord.py uses function decorators to assign commands
    import secret_santa_bot.bot.santa  # pylint: disable=import-outside-toplevel

    secret_santa_bot.bot.santa.main(vault.read_secret_token())


if __name__ == '__main__':
    main()
