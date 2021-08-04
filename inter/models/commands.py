"""
This file implements the command models found at
https://discord.com/developers/docs/interactions/slash-commands#application-command-object.
"""
from __future__ import annotations

import enum
from typing import List, Optional, Union

from pydantic import BaseModel

from .discord import snowflake

__all__ = ('Command', 'CommandOption', 'CommandOptionType', 'CommandOptionChoice')


class Command(BaseModel):
    id: snowflake
    application_id: snowflake
    guild_id: Optional[snowflake]
    name: str
    description: str
    options: Optional[List[CommandOption]]
    default_permission: Optional[bool]


class CommandOption(BaseModel):
    type: CommandOptionType
    name: str
    description: str
    required: Optional[bool]
    choices: Optional[List[CommandOptionChoice]]
    options: Optional[CommandOption]


class CommandOptionType(enum.IntEnum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9


class CommandOptionChoice(BaseModel):
    name: str
    value: Union[int, str]
