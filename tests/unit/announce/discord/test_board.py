"""
:Copyright: 2014-2023 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from flask import Flask

from byceps.announce.connections import build_announcement_request
from byceps.events.board import BoardPostingCreatedEvent, BoardTopicCreatedEvent
from byceps.services.board.models import (
    BoardCategoryID,
    BoardID,
    PostingID,
    TopicID,
)
from byceps.services.webhooks.models import OutgoingWebhook
from byceps.typing import BrandID, UserID

from tests.helpers import generate_token, generate_uuid

from .helpers import build_announcement_request_for_discord, build_webhook, now


OCCURRED_AT = now()
BRAND_ID = BrandID('acmecon')
BRAND_TITLE = 'ACME Entertainment Convention'
BOARD_ID = BoardID(generate_token())
CATEGORY_1_ID = BoardCategoryID(generate_uuid())
CATEGORY_1_TITLE = 'Kategorie 1'
CATEGORY_2_ID = BoardCategoryID(generate_uuid())
CATEGORY_2_TITLE = 'Kategorie 2'
TOPIC_ID = TopicID(generate_uuid())
POSTING_ID = PostingID(generate_uuid())
MODERATOR_ID = UserID(generate_uuid())
MODERATOR_SCREEN_NAME = 'TheModerator'
USER_ID = UserID(generate_uuid())

WEBHOOK_URL = 'https://webhoooks.test/board'


def test_announce_topic_created(app: Flask):
    expected_url = f'https://website.test/board/topics/{TOPIC_ID}'
    expected_content = (
        '[Forum] RocketRandy hat das Thema '
        '"Cannot connect to the party network :(" erstellt: '
        f'<{expected_url}>'
    )
    expected = build_announcement_request_for_discord(
        WEBHOOK_URL, expected_content
    )

    event = BoardTopicCreatedEvent(
        occurred_at=OCCURRED_AT,
        initiator_id=USER_ID,
        initiator_screen_name='RocketRandy',
        brand_id=BRAND_ID,
        brand_title=BRAND_TITLE,
        board_id=BOARD_ID,
        topic_id=TOPIC_ID,
        topic_creator_id=USER_ID,
        topic_creator_screen_name='RocketRandy',
        topic_title='Cannot connect to the party network :(',
        url=expected_url,
    )

    webhook = build_board_webhook(BOARD_ID)

    assert build_announcement_request(event, webhook) == expected


def test_announce_posting_created(app: Flask):
    expected_url = f'https://website.test/board/postings/{POSTING_ID}'
    expected_content = (
        '[Forum] RocketRandy hat auf das Thema '
        '"Cannot connect to the party network :(" geantwortet: '
        f'<{expected_url}>'
    )
    expected = build_announcement_request_for_discord(
        WEBHOOK_URL, expected_content
    )

    event = BoardPostingCreatedEvent(
        occurred_at=OCCURRED_AT,
        initiator_id=USER_ID,
        initiator_screen_name='RocketRandy',
        brand_id=BRAND_ID,
        brand_title=BRAND_TITLE,
        board_id=BOARD_ID,
        posting_creator_id=USER_ID,
        posting_creator_screen_name='RocketRandy',
        posting_id=POSTING_ID,
        topic_id=TOPIC_ID,
        topic_title='Cannot connect to the party network :(',
        topic_muted=False,
        url=expected_url,
    )

    webhook = build_board_webhook(BOARD_ID)

    assert build_announcement_request(event, webhook) == expected


# helpers


def build_board_webhook(board_id: BoardID) -> OutgoingWebhook:
    return build_webhook(
        event_types={
            'board-posting-created',
            'board-topic-created',
        },
        event_filters={
            'board-posting-created': {'board_id': [str(board_id)]},
            'board-topic-created': {'board_id': [str(board_id)]},
        },
        text_prefix='[Forum] ',
        url=WEBHOOK_URL,
    )
