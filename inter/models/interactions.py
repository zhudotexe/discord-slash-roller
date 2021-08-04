"""
This file implements the interaction models found at
https://discord.com/developers/docs/interactions/slash-commands#interaction-object.
"""
import enum
from typing import Any, List, Mapping, Optional, Union

from pydantic import BaseModel

from .commands import CommandOptionType
from .components import Component
from .discord import AllowedMentions, ChannelType, Embed, Member, PartialMember, Role, User, snowflake

__all__ = (
    'Interaction', 'InteractionType',
    'InteractionResponse', 'InteractionCallbackType', 'InteractionCommandCallbackData',
    'InteractionCommandCallbackDataFlags'
)


# ==== inbound ====
class InteractionType(enum.IntEnum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3


class PartialChannel(BaseModel):
    id: snowflake
    name: str
    type: ChannelType
    permissions: Any


class CommandInteractionDataResolved(BaseModel):
    users: Optional[Mapping[snowflake, User]]
    members: Optional[Mapping[snowflake, PartialMember]]
    roles: Optional[Mapping[snowflake, Role]]
    channels: Optional[Mapping[snowflake, PartialChannel]]


class CommandInteractionDataOption(BaseModel):
    name: str
    type: CommandOptionType
    value: Optional[Union[bool, int, snowflake, str]]
    options: Optional[List['CommandInteractionData']]


class CommandInteractionData(BaseModel):
    id: snowflake
    name: str
    resolved: Optional[CommandInteractionDataResolved]
    options: Optional[List[CommandInteractionDataOption]]
    custom_id: Optional[str]
    component_type: Optional[int]


class Interaction(BaseModel):
    id: snowflake
    application_id: snowflake
    type: InteractionType
    data: Optional[CommandInteractionData]
    guild_id: Optional[snowflake]
    channel_id: Optional[snowflake]
    member: Optional[Member]
    user: Optional[User]
    token: str
    version: int
    message: Optional[dict]  # todo implement message here


CommandInteractionDataOption.update_forward_refs()


# ==== outbound ====
class InteractionCallbackType(enum.IntEnum):
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    DEFERRED_UPDATE_MESSAGE = 6
    UPDATE_MESSAGE = 7


class InteractionCommandCallbackDataFlags(enum.IntFlag):
    EPHEMERAL = 1 << 6


class InteractionCommandCallbackData(BaseModel):
    tts: Optional[bool]
    content: Optional[str]
    embeds: Optional[List[Embed]]
    allowed_mentions: Optional[AllowedMentions]
    flags: Optional[InteractionCommandCallbackDataFlags]
    components: Optional[Component]


class InteractionResponse(BaseModel):
    type: InteractionCallbackType
    data: Optional[InteractionCommandCallbackData]


class MessageInteraction(BaseModel):
    id: snowflake
    type: InteractionType
    name: str
    user: User
