"""
byceps.announce.helpers
~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2020 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from typing import Any, Dict, List, Optional

from flask import current_app
import requests

from ..events.base import _BaseEvent
from ..services.webhooks import service as webhook_service
from ..services.webhooks.transfer.models import OutgoingWebhook

from .events import get_name_for_event


def get_screen_name_or_fallback(screen_name: Optional[str]) -> str:
    """Return the screen name or a fallback value."""
    return screen_name if screen_name else 'Jemand'


def get_webhooks(event: _BaseEvent) -> List[OutgoingWebhook]:
    event_name = get_name_for_event(event)
    webhooks = webhook_service.get_enabled_outgoing_webhooks(event_name)

    # Stable order is easier to test.
    webhooks.sort(key=lambda wh: wh.extra_fields.get('channel', ''))

    return webhooks


def matches_selectors(
    event: _BaseEvent,
    webhook: OutgoingWebhook,
    attribute_name: str,
    actual_value: str,
) -> bool:
    event_name = get_name_for_event(event)
    if event_name not in webhook.event_selectors:
        # This should not happen as only webhooks supporting this
        # event type should have been selected before calling an
        # event announcement handler.
        return False

    event_selector = webhook.event_selectors.get(event_name)
    if event_selector is None:
        # If no specific matcher rule is defined, a value of `None`
        # is okay (as it allows the event name to be contained in
        # the dictionary as a key).
        event_selector = {}

    allowed_values = event_selector.get(attribute_name)
    return (allowed_values is None) or (actual_value in allowed_values)


def call_webhook(webhook: OutgoingWebhook, text: str) -> None:
    """Send HTTP request to the webhook."""
    text_prefix = webhook.text_prefix
    if text_prefix:
        text = text_prefix + text

    data = _assemble_request_data(webhook, text)

    requests.post(webhook.url, json=data)  # Ignore response code for now.


def _assemble_request_data(
    webhook: OutgoingWebhook, text: str
) -> Dict[str, Any]:
    if webhook.format == 'discord':
        return {'content': text}

    elif webhook.format == 'weitersager':
        channel = webhook.extra_fields.get('channel')
        if not channel:
            current_app.logger.warning(
                f'No channel specified with IRC webhook.'
            )

        return {'channel': channel, 'text': text}
