"""The main logic of SecretSantaBot. Contains commands and their associated
helper functions."""
# pyright: reportUnusedClass=false
from __future__ import annotations

import hikari
import lightbulb


def main(discord_authentication_token: str, /) -> None:
    bot = hikari.GatewayBot(discord_authentication_token)
    client = lightbulb.client_from_app(bot)
    bot.subscribe(hikari.StartingEvent, client.start)

    @client.register()
    class Ping(  # pylint: disable=unused-variable
        lightbulb.SlashCommand,
        name="ping",
        description="checks the bot is alive",
    ):

        @lightbulb.invoke
        async def invoke(self, ctx: lightbulb.Context) -> None:
            await ctx.respond("Pong!")

    bot.run()
