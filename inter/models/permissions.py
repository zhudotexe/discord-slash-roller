"""
This file implements the command permission models found at
https://discord.com/developers/docs/interactions/slash-commands#application-command-permissions-object.
"""
import enum
from typing import List

from pydantic import BaseModel

from .discord import snowflake

__all__ = ('CommandPermissionType', 'CommandPermissions', 'GuildCommandPermissions')


class CommandPermissionType(enum.IntEnum):
    ROLE = 1
    USER = 2


class CommandPermissions(BaseModel):
    id: snowflake
    type: CommandPermissionType
    permission: bool


class GuildCommandPermissions(BaseModel):
    id: snowflake
    application_id: snowflake
    guild_id: snowflake
    permissions: List[CommandPermissions]
