"""
:Copyright: 2014-2023 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from flask import Flask

from byceps.announce.connections import build_announcement_request
from byceps.events.news import NewsItemPublishedEvent
from byceps.services.news.models import NewsChannelID, NewsItemID
from byceps.services.webhooks.models import OutgoingWebhook
from byceps.typing import UserID

from tests.helpers import generate_token, generate_uuid

from .helpers import build_announcement_request_for_discord, build_webhook, now


OCCURRED_AT = now()
ADMIN_ID = UserID(generate_uuid())
NEWS_CHANNEL_ID = NewsChannelID(generate_token())
NEWS_ITEM_ID = NewsItemID(generate_uuid())

WEBHOOK_URL = 'https://webhoooks.test/news'


def test_published_news_item_announced_with_url(app: Flask) -> None:
    expected_content = (
        '[News] Die News "Zieh dir das mal rein!" wurde veröffentlicht. '
        'https://www.acmecon.test/news/zieh-dir-das-mal-rein'
    )
    expected = build_announcement_request_for_discord(
        WEBHOOK_URL, expected_content
    )

    event = NewsItemPublishedEvent(
        occurred_at=OCCURRED_AT,
        initiator_id=ADMIN_ID,
        initiator_screen_name='Admin',
        item_id=NEWS_ITEM_ID,
        channel_id=NEWS_CHANNEL_ID,
        published_at=OCCURRED_AT,
        title='Zieh dir das mal rein!',
        external_url='https://www.acmecon.test/news/zieh-dir-das-mal-rein',
    )

    webhook = build_news_webhook()

    assert build_announcement_request(event, webhook) == expected


def test_published_news_item_announced_without_url(app: Flask) -> None:
    expected_content = (
        '[News] Die News "Zieh dir auch das rein!" wurde veröffentlicht.'
    )
    expected = build_announcement_request_for_discord(
        WEBHOOK_URL, expected_content
    )

    event = NewsItemPublishedEvent(
        occurred_at=OCCURRED_AT,
        initiator_id=ADMIN_ID,
        initiator_screen_name='Admin',
        item_id=NEWS_ITEM_ID,
        channel_id=NEWS_CHANNEL_ID,
        published_at=OCCURRED_AT,
        title='Zieh dir auch das rein!',
        external_url=None,
    )

    webhook = build_news_webhook()

    assert build_announcement_request(event, webhook) == expected


# helpers


def build_news_webhook() -> OutgoingWebhook:
    return build_webhook(
        event_types={'news-item-published'},
        event_filters={
            'news-item-published': {'channel_id': [str(NEWS_CHANNEL_ID)]}
        },
        text_prefix='[News] ',
        url=WEBHOOK_URL,
    )
