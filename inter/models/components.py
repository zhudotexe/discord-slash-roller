"""
This file implements the message component models found at
https://discord.com/developers/docs/interactions/message-components.
"""
from __future__ import annotations

import enum
from typing import List, Optional

from pydantic import BaseModel

from .discord import snowflake

__all__ = ('ComponentType', 'Component', 'ActionRow', 'Button', 'SelectMenu')


class ComponentType(enum.IntEnum):
    ACTION_ROW = 1
    BUTTON = 2
    SELECT_MENU = 3


class Component(BaseModel):
    type: ComponentType


class ActionRow(Component):
    type = ComponentType.ACTION_ROW
    components: List[Component]


# ==== Button ====
class PartialEmoji(BaseModel):
    name: Optional[str]
    id: Optional[snowflake]
    animated: Optional[bool]


class ButtonStyle(enum.IntEnum):
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5


class Button(Component):
    type = ComponentType.BUTTON
    style: ButtonStyle
    label: Optional[str]
    emoji: Optional[PartialEmoji]
    custom_id: Optional[str]
    url: Optional[str]
    disabled: Optional[bool]


# ==== Select Menu ====
class SelectOption(BaseModel):
    label: str
    value: str
    description: Optional[str]
    emoji: Optional[PartialEmoji]
    default: Optional[bool]


class SelectMenu(Component):
    type = ComponentType.SELECT_MENU
    custom_id: str
    options: List[SelectOption]
    placeholder: Optional[str]
    min_values: Optional[int]
    max_values: Optional[int]
    disabled: Optional[bool]
