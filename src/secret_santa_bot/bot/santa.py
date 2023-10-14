"""The main logic of SecretSantaBot. Contains commands and their associated
helper functions."""
from __future__ import annotations

import asyncio
import logging
import typing

import hikari

from secret_santa_bot.bot import chains_of_primes

if typing.TYPE_CHECKING:
    import concurrent.futures
    import os
    from hikari.internal import data_binding
    from hikari import intents as intents_
    from hikari.impl import config as config_impl


_logger = logging.getLogger(__name__)
_logger.handlers = logging.getLogger('hikari').handlers


def get_super_dir(object_: object):
    super_attributes = set()
    for base_class in object_.__class__.__bases__:
        super_attributes.update(dir(base_class))
    return super_attributes


class CommandRegistrationMixin(hikari.GatewayBot):
    """A Mixin designed to register all bot commands of the lowest subclass.
    The registration invokes self.listen() on each public method (i.e., any
    method not prepended with _ or __)."""

    def __init__(
        self,
        token: str,
        *,
        allow_color: bool = True,
        banner: typing.Optional[str] = 'hikari',
        suppress_optimization_warning: bool = False,
        executor: typing.Optional[concurrent.futures.Executor] = None,
        force_color: bool = False,
        cache_settings: typing.Optional[config_impl.CacheSettings] = None,
        http_settings: typing.Optional[config_impl.HTTPSettings] = None,
        dumps: data_binding.JSONEncoder = data_binding.default_json_dumps,
        loads: data_binding.JSONDecoder = data_binding.default_json_loads,
        intents: intents_.Intents = intents_.Intents.ALL_UNPRIVILEGED,
        auto_chunk_members: bool = True,
        logs: typing.Union[
            None, str, int, typing.Dict[str, typing.Any], os.PathLike[str]
        ] = 'INFO',
        max_rate_limit: float = 300.0,
        max_retries: int = 3,
        proxy_settings: typing.Optional[config_impl.ProxySettings] = None,
        rest_url: typing.Optional[str] = None,
    ):
        super().__init__(
            token,
            allow_color=allow_color,
            banner=banner,
            suppress_optimization_warning=suppress_optimization_warning,
            executor=executor,
            force_color=force_color,
            cache_settings=cache_settings,
            http_settings=http_settings,
            dumps=dumps,
            loads=loads,
            intents=intents,
            auto_chunk_members=auto_chunk_members,
            logs=logs,
            max_rate_limit=max_rate_limit,
            max_retries=max_retries,
            proxy_settings=proxy_settings,
            rest_url=rest_url,
        )
        self.register_commands()

    def register_commands(self):
        super_dir = get_super_dir(self)
        local_methods = [
            method for method in dir(self) if method not in super_dir
        ]
        for method in local_methods:
            if not method.startswith('_'):
                self.listen()(getattr(self, method))


class SecretSantaBot(CommandRegistrationMixin):

    async def ping(self, event: hikari.GuildMessageCreateEvent) -> None:
        """If a non-bot user @ mentions your bot, respond with 'Pong!'."""
        if not event.is_human:
            return
        me = self.get_me()
        if me.id in event.message.user_mentions_ids:
            await event.message.respond('Pong!')


class Santa:
    __slots__ = ['member', 'target', 'receive']

    def __init__(self, member: discord.Member):
        self.member: discord.Member = member
        self.target: discord.Member | None = None


async def _message_santa(santa: Santa, role_name: str) -> None:
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
    except discord.errors.Forbidden as e:
        _logger.error(
            'Unable to message "%s". The user may have messaging from '
            'non-friend server members disabled.',
            santa.member.name,
        )
        raise e from None
    except (discord.HTTPException, TypeError) as e:
        _logger.exception('Unknown error occurred:', exc_info=e)
        raise e
    except AttributeError as e:
        _logger.critical(
            'SecretSantaBot is in the role @%s. The generated secret santa '
            'groups are invalid as SecretSantaBot does not own capital D:',
            role_name,
        )
        raise e from None


def _create_santas(role: discord.Role) -> list[Santa]:
    santas = [Santa(member) for member in role.members]
    santas.sort(key=lambda santa: santa.member.id)
    return santas


async def _message_santas(role: discord.Role):
    santas = _create_santas(role)
    santas = chains_of_primes.assign_santas(santas)
    messages = [_message_santa(santa, role.name) for santa in santas]
    return await asyncio.gather(*messages)


async def secret_santa(interaction: discord.Interaction, role: discord.Role):
    """Required permission: Server Members Intent

    Args:
        interaction:
        role: A role defined within a discord guild. This should not include
            the bot, otherwise the bot will be included in the gift givers.

    Returns:

    """
    guild_owner = interaction.guild.owner_id if interaction.guild else object()
    command_invoker = interaction.user.id
    if guild_owner == command_invoker:
        try:
            await _message_santas(role)
        except ValueError:
            response_message = (
                f'Error: Only one participant found in role @{role.name}.'
            )
        except discord.Forbidden:
            response_message = 'Error during messaging. Check log for details.'
        except (discord.HTTPException, TypeError):
            response_message = 'Unknown error occurred. Check log for details.'
        except AttributeError:
            response_message = (
                f'CRITICAL ERROR: SecretSantaBot cannot give gifts. Remove '
                f'SecretSantaBot from @{role.name} and generate again.'
            )
        else:
            response_message = 'Santas successfully messaged.'
        await interaction.response.send_message(
            response_message, ephemeral=True
        )
    else:
        await interaction.response.send_message(
            'Only the owner may roll for secret santa', ephemeral=True
        )


def main(discord_authentication_token: str, /) -> None:
    """Runs the SecretSantaBot. This function is locking."""
    bot = SecretSantaBot(token=discord_authentication_token)
    del discord_authentication_token
    bot.run()
