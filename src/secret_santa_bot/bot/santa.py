"""The main logic of SecretSantaBot. Contains commands and their associated
helper functions."""
from __future__ import annotations

import asyncio
import logging
import os
from typing import Any

import discord
from discord.ext import commands

from secret_santa_bot.bot import chains_of_primes


# TODO: Find minimum set of permissions required
class Bot(commands.Bot):
    """Sets "/" and default intents required by SecretSantaBot"""

    def __init__(
        self,
        command_prefix: commands.bot.PrefixType[commands.bot.BotT] | None = None,  # type: ignore # Ignored due to a bug in type hints of discord.py # pylint: disable=line-too-long
        *,
        intents: discord.Intents | None = None,
        **options: Any,
    ):
        if not command_prefix:
            command_prefix = '/'
        if not intents:
            intents = discord.Intents.default()
            intents.members = True
        super().__init__(command_prefix, intents=intents, **options)


bot = Bot()


class Santa:
    __slots__ = ['member', 'target', 'receive']

    def __init__(self, member: discord.Member):
        self.member: discord.Member = member
        self.target: discord.Member | None = None


@bot.event
async def on_ready() -> None:
    """Required permissions: None"""
    await bot.tree.sync(guild=discord.Object(id=os.environ['GUILD_ID']))
    print('Bot is ready to bot it up')


async def _message_santa(santa: Santa) -> bool:
    successful = False
    try:
        await santa.member.send(
            (
                f'You will be giving a gift to {santa.target}\nNote '
                f'that this is their discord name and not the name that will '
                f'be within the rules and information file\nThe rules and '
                f'information for this year along with the addresses of '
                f'everyone will be in the Secret Santa thread within the '
                f'{santa.member.guild.name} server. The thread may close after '
                f'a time but can still be viewed by clicking on the threads '
                f'button -> Archived -> Private'
            )
        )
        successful = True
    except discord.errors.Forbidden:
        logging.error(
            'Unable to message "%s". The user may have messaging from '
            'non-friend server members disabled.',
            {santa.member.name},
        )
    except AttributeError:
        # Bot attempts to message itself
        successful = True
    return successful


def _create_santas(role: discord.Role) -> list[Santa]:
    santas = [Santa(member) for member in role.members]
    santas.sort(key=lambda santa: santa.member.id)
    return santas


async def _message_santas(role: discord.Role):
    santas = _create_santas(role)
    santas = chains_of_primes.assign_santas(santas)
    messages = [_message_santa(santa) for santa in santas]
    return await asyncio.gather(*messages)


@bot.tree.command(guild=discord.Object(id=os.environ['GUILD_ID']))
async def secret_santa(interaction: discord.Interaction, role: discord.Role):
    """Required permissions:"""
    if interaction.guild:
        guild_owner = interaction.guild.owner_id
    else:
        guild_owner = object()
    command_invoker = interaction.user.id
    if guild_owner == command_invoker:
        message_successful = await _message_santas(role)
        if not all(message_successful):
            response_message = 'Santas successfully messaged.'
        else:
            response_message = 'Error during operation. Check log for details.'
        await interaction.response.send_message(
            response_message, ephemeral=True
        )
    else:
        await interaction.response.send_message(
            'Only the owner can roll for secret santa', ephemeral=True
        )


def main(discord_authentication_token: str, /) -> None:
    """Runs the SecretSantaBot. This function is locking."""
    bot.run(discord_authentication_token)
