"""Sets enviornment variables for secret_santa_bot. Notably, reading the token
used by the bot."""
import os

from secret_santa_bot import _vault


def main():
    vault: _vault.Vault = _vault.Vault(
        url=os.environ['VAULT_PATH'], token=os.environ['VAULT_TOKEN']
    )
    os.environ['GUILD_ID'] = vault.read_secret_token(username='GUILD_ID')
    discord_authentication_token: str = vault.read_secret_token()
    import secret_santa_bot.bot.santa

    secret_santa_bot.bot.santa.main(discord_authentication_token)


if __name__ == '__main__':
    main()
