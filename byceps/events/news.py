"""
byceps.events.news
~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2021 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from dataclasses import dataclass
from datetime import datetime

from ..services.news.transfer.models import ChannelID, ItemID

from .base import _BaseEvent


@dataclass(frozen=True)
class NewsItemPublished(_BaseEvent):
    item_id: ItemID
    channel_id: ChannelID
    published_at: datetime
    title: str
    external_url: str
