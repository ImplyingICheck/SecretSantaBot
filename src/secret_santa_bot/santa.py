import os
import sys
from collections.abc import Iterable

import discord
from discord.ext import commands

from secret_santa_bot import chains_of_primes

_MY_GUILD = os.environ["GUILD_ID"]
# TODO: Find minimum set of permissions required
bot: commands.Bot = commands.Bot(
    command_prefix="/", intents=discord.Intents.default()
)


class Santa:
    __slots__ = ["member", "target", "receive"]

    def __init__(self, member: discord.Member):
        self.member: discord.Member = member
        self.target: discord.Member | None = None


@bot.event
async def on_ready() -> None:
    """Required permissions: None"""
    await bot.tree.sync(guild=discord.Object(id=_MY_GUILD))
    print("Bot is ready to bot it up")


async def message_santas(santas: Iterable[Santa]) -> None:
    for santa in santas:
        member = santa.member
        await member.send(
            (
                f"You will be giving a gift to {santa.target}\nNote "
                f"that this is their discord name and not the name that will "
                f"be within the rules and information file\nThe rules and "
                f"information for this year along with the addresses of "
                f"everyone will be in the Secret Santa thread within the "
                f"{member.guild.name} server. The thread may close after a time"
                f" but can still be viewed by clicking on the threads button ->"
                f" Archived -> Private"
            )
        )


@bot.tree.command(guild=discord.Object(id=_MY_GUILD))
async def santa(interaction: discord.Interaction, role: discord.Role):
    """Required permissions: View Channels, Send Messages, Read Messages/View Channels
    Intents.message_content"""
    if interaction.guild:
        guild_owner = interaction.guild.owner_id
    else:
        guild_owner = object()
    command_invoker = interaction.user.id
    if guild_owner == command_invoker:
        santas = [Santa(member) for member in role.members]
        santas.sort(key=lambda santa: santa.member.id)
        santas = chains_of_primes.assign_santas(santas)
        await message_santas(santas)
    else:
        await interaction.response.send_message(
            "Only the owner can roll for secret santa"
        )


def main(discord_authentication_token: str, /) -> None:
    """Runs the SecretSantaBot. This function is locking."""
    bot.run(discord_authentication_token)
