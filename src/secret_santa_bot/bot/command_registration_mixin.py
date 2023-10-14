from __future__ import annotations

import concurrent.futures
import os
import typing

import hikari
from hikari import intents as intents_
from hikari.impl import config as config_impl
from hikari.internal import data_binding

from secret_santa_bot.bot.santa import get_super_dir


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
