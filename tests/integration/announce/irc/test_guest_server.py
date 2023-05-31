"""
:Copyright: 2014-2023 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from flask import Flask

from byceps.announce.connections import build_announcement_request
from byceps.events.guest_server import GuestServerRegisteredEvent
from byceps.services.guest_server.models import ServerID
from byceps.services.party.models import Party
from byceps.services.user.models.user import User

from tests.helpers import generate_uuid

from .helpers import build_announcement_request_for_irc, now


OCCURRED_AT = now()


def test_guest_server_registered(
    admin_app: Flask, party: Party, admin_user: User, user, webhook_for_irc
):
    expected_text = 'Admin hat einen Gastserver von User für die Party "ACMECon 2014" registriert.'
    expected = build_announcement_request_for_irc(expected_text)

    event = GuestServerRegisteredEvent(
        occurred_at=OCCURRED_AT,
        initiator_id=admin_user.id,
        initiator_screen_name=admin_user.screen_name,
        party_id=party.id,
        party_title=party.title,
        owner_id=user.id,
        owner_screen_name=user.screen_name,
        server_id=ServerID(generate_uuid()),
    )

    assert build_announcement_request(event, webhook_for_irc) == expected
