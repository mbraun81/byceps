"""
byceps.announce.handlers.auth
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Announce auth events.

:Copyright: 2014-2023 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from __future__ import annotations

from flask_babel import gettext

from byceps.announce.helpers import (
    Announcement,
    get_screen_name_or_fallback,
    with_locale,
)
from byceps.events.auth import UserLoggedIn
from byceps.services.site import site_service
from byceps.services.webhooks.models import OutgoingWebhook


@with_locale
def announce_user_logged_in(
    event: UserLoggedIn, webhook: OutgoingWebhook
) -> Announcement | None:
    """Announce that a user has logged in."""
    screen_name = get_screen_name_or_fallback(event.initiator_screen_name)

    site = None
    if event.site_id:
        site = site_service.find_site(event.site_id)

    if site:
        text = gettext(
            '%(screen_name)s has logged in on site "%(site_title)s".',
            screen_name=screen_name,
            site_title=site.title,
        )
    else:
        text = gettext(
            '%(screen_name)s has logged in.', screen_name=screen_name
        )

    return Announcement(text)
