"""
This file represents miscellaneous types defined by Discord.
"""
import datetime
import enum
from typing import List, Optional

from pydantic import BaseModel

__all__ = (
    'snowflake', 'User', 'PartialMember', 'Member', 'Role', 'Channel', 'ChannelType', 'Embed', 'AllowedMentions'
)

snowflake = str


# ==== User ====
class User(BaseModel):
    id: snowflake
    username: str
    discriminator: str
    avatar: Optional[str]
    bot: Optional[bool]
    system: Optional[bool]
    mfa_enabled: Optional[bool]
    locale: Optional[str]
    verified: Optional[bool]
    email: Optional[str]
    flags: Optional[int]
    premium_type: Optional[int]
    public_flags: Optional[int]


# ==== Member ====
class PartialMember(BaseModel):
    nick: Optional[str]
    roles: List[snowflake]
    joined_at: datetime.datetime
    premium_since: Optional[datetime.datetime]
    pending: Optional[bool]  # always included in GUILD_ events
    permissions: Optional[str]  # included when inside the interaction object


class Member(PartialMember):
    user: Optional[User]  # not included in MESSAGE_CREATE and MESSAGE_UPDATE events
    deaf: bool
    mute: bool


# ==== Role ====
class RoleTags(BaseModel):
    bot_id: Optional[snowflake]
    integration_id: Optional[snowflake]
    premium_subscriber: Optional[bool]


class Role(BaseModel):
    id: snowflake
    name: str
    color: int
    hoist: bool
    position: int
    permissions: str
    managed: bool
    mentionable: bool
    tags: Optional[RoleTags]


# ==== Channel ====
class ChannelType(enum.IntEnum):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_NEWS = 5
    GUILD_STORE = 6
    GUILD_NEWS_THREAD = 10
    GUILD_PUBLIC_THREAD = 11
    GUILD_PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13


class PermissionOverwrite(BaseModel):
    id: snowflake
    type: int
    allow: str
    deny: str


class ThreadMetadata(BaseModel):
    archived: bool
    auto_archive_duration: int
    archive_timestamp: datetime.datetime
    locked: Optional[bool]


class ThreadMember(BaseModel):
    id: Optional[snowflake]
    user_id: Optional[snowflake]
    join_timestamp: datetime.datetime
    flags: int


class Channel(BaseModel):
    id: snowflake
    type: ChannelType
    guild_id: Optional[snowflake]
    position: Optional[int]
    permission_overwrites: Optional[List[PermissionOverwrite]]
    name: Optional[str]
    topic: Optional[str]
    nsfw: Optional[bool]
    last_message_id: Optional[snowflake]
    bitrate: Optional[int]
    user_limit: Optional[int]
    rate_limit_per_user: Optional[int]
    recipients: Optional[List[User]]
    icon: Optional[str]
    owner_id: Optional[snowflake]
    application_id: Optional[snowflake]
    parent_id: Optional[snowflake]
    rtc_region: Optional[str]
    video_quality_mode: Optional[int]
    message_count: Optional[int]
    thread_metadata: Optional[ThreadMetadata]
    member: Optional[ThreadMember]
    default_auto_archive_duration: Optional[int]


# ==== Embed ====
class EmbedThumbnail(BaseModel):
    url: Optional[str]
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]


class EmbedVideo(BaseModel):
    url: Optional[str]
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]


class EmbedImage(BaseModel):
    url: Optional[str]
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]


class EmbedProvider(BaseModel):
    name: Optional[str]
    url: Optional[str]


class EmbedAuthor(BaseModel):
    name: Optional[str]
    url: Optional[str]
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]


class EmbedFooter(BaseModel):
    text: str
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]


class EmbedField(BaseModel):
    name: str
    value: str
    inline: Optional[bool]


class Embed(BaseModel):
    title: Optional[str]
    type: Optional[str] = 'rich'
    description: Optional[str]
    url: Optional[str]
    timestamp: Optional[datetime.datetime]
    color: Optional[int]
    footer: Optional[EmbedFooter]
    image: Optional[EmbedImage]
    thumbnail: Optional[EmbedThumbnail]
    video: Optional[EmbedVideo]
    provider: Optional[EmbedProvider]
    author: Optional[EmbedAuthor]
    fields: Optional[List[EmbedField]]


# ==== Message ====
# class Message(BaseModel):
#     id: snowflake
#     channel_id: snowflake
#     guild_id: Optional[snowflake]
#     author: User
#     member: Optional[PartialMember]
#     content: str
#     timestamp: datetime.datetime
#     edited_timestamp: Optional[datetime.datetime]
#     tts: bool
#     mention_everyone: bool
#     mentions: List[User]
#     mention_roles: List[snowflake]
#     mention_channels: List[ChannelMention]
#     attachments: List[Attachment]
#     embeds: List[Embed]
#     reactions: Optional[List[Reaction]]
#     nonce: Optional[Union[int, str]]
#     pinned: bool
#     webhook_id: Optional[snowflake]
#     type: int

# ==== AllowedMentions ====
class AllowedMentions(BaseModel):
    parse: Optional[List[str]]
    roles: Optional[List[snowflake]]
    users: Optional[List[snowflake]]
    replied_user: Optional[bool]
