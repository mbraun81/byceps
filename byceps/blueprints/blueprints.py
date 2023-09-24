"""
byceps.application.blueprints.blueprints
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2014-2023 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Optional

from flask import Flask
import structlog

from byceps.util.framework.blueprint import get_blueprint


log = structlog.get_logger()


BlueprintReg = tuple[str, Optional[str]]


def register_blueprints(app: Flask) -> None:
    """Register blueprints depending on the configuration."""
    for name, url_prefix in _get_blueprints(app):
        blueprint = get_blueprint(name)
        app.register_blueprint(blueprint, url_prefix=url_prefix)


def _get_blueprints(app: Flask) -> Iterator[BlueprintReg]:
    """Yield blueprints to register on the application."""
    app_mode = app.byceps_app_mode

    if app_mode.is_admin() or app_mode.is_site():
        yield from _get_blueprints_common()

    if app_mode.is_admin():
        yield from _get_blueprints_admin()
        log.info('Admin blueprints: enabled')
    else:
        log.info('Admin blueprints: disabled')

    if app_mode.is_site():
        yield from _get_blueprints_site()
        log.info('Site blueprints: enabled')
    else:
        log.info('Site blueprints: disabled')

    yield ('monitoring.healthcheck', '/health')

    if app.config['METRICS_ENABLED']:
        yield ('monitoring.metrics', '/metrics')
        log.info('Metrics: enabled')
    else:
        log.info('Metrics: disabled')

    if (app_mode.is_admin() or app_mode.is_site()) and app.config.get(
        'STYLE_GUIDE_ENABLED', False
    ):
        yield ('common.style_guide', '/style_guide')
        log.info('Style guide: enabled')
    else:
        log.info('Style guide: disabled')


def _get_blueprints_common() -> Iterator[BlueprintReg]:
    yield from [
        ('common.authentication.password', '/authentication/password'),
        ('common.core', None),
        ('common.guest_server', None),
        ('common.locale', '/locale'),
    ]


def _get_blueprints_site() -> Iterator[BlueprintReg]:
    yield from [
        ('site.attendance', '/attendance'),
        ('site.authentication.login', '/authentication'),
        ('site.board', '/board'),
        (
            'site.connected_external_accounts.discord',
            '/connected_external_accounts/discord',
        ),
        ('site.consent', '/consent'),
        ('site.core', None),
        ('site.dashboard', '/dashboard'),
        ('site.guest_server', '/guest_servers'),
        ('site.homepage', '/'),
        ('site.news', '/news'),
        ('site.newsletter', '/newsletter'),
        ('site.orga_team', '/orgas'),
        ('site.page', None),
        ('site.party_history', '/party_history'),
        ('site.seating', '/seating'),
        ('site.shop.order', '/shop'),
        ('site.shop.orders', '/shop/orders'),
        ('site.site', None),
        ('site.snippet', None),
        ('site.ticketing', '/tickets'),
        ('site.tourney', '/tourneys'),
        ('site.user.avatar', '/users'),
        ('site.user.creation', '/users'),
        ('site.user.current', '/users'),
        ('site.user.settings', '/users/me/settings'),
        ('site.user.email_address', '/users/email_address'),
        ('site.user_profile', '/users'),
        ('site.user_badge', '/user_badges'),
        ('site.user_group', '/user_groups'),
        ('site.user_message', '/user_messages'),
    ]


def _get_blueprints_admin() -> Iterator[BlueprintReg]:
    yield from [
        ('admin.api', '/admin/api'),
        ('admin.attendance', '/admin/attendance'),
        ('admin.authentication.login', '/authentication'),
        ('admin.authorization', '/admin/authorization'),
        ('admin.board', '/admin/boards'),
        ('admin.brand', '/admin/brands'),
        ('admin.consent', '/admin/consent'),
        ('admin.core', '/'),
        ('admin.dashboard', '/admin/dashboard'),
        ('admin.guest_server', '/admin/guest_servers'),
        ('admin.jobs', '/admin/jobs'),
        ('admin.language', '/admin/languages'),
        ('admin.maintenance', '/admin/maintenance'),
        ('admin.more', '/admin/more'),
        ('admin.news', '/admin/news'),
        ('admin.newsletter', '/admin/newsletter'),
        ('admin.orga', '/admin/orgas'),
        ('admin.orga_presence', '/admin/presence'),
        ('admin.orga_team', '/admin/orga_teams'),
        ('admin.page', '/admin/pages'),
        ('admin.party', '/admin/parties'),
        ('admin.seating', '/admin/seating'),
        ('admin.shop', None),
        ('admin.shop.article', '/admin/shop/articles'),
        ('admin.shop.catalog', '/admin/shop/catalogs'),
        ('admin.shop.email', '/admin/shop/email'),
        ('admin.shop.order', '/admin/shop/orders'),
        ('admin.shop.cancelation_request', '/admin/shop/cancelation_requests'),
        ('admin.shop.shipping', '/admin/shop/shipping'),
        ('admin.shop.shop', '/admin/shop/shop'),
        ('admin.shop.storefront', '/admin/shop/storefronts'),
        ('admin.site', '/admin/sites'),
        ('admin.site.navigation', '/admin/sites/navigation'),
        ('admin.snippet', '/admin/snippets'),
        ('admin.ticketing', '/admin/ticketing'),
        ('admin.ticketing.category', '/admin/ticketing/categories'),
        ('admin.ticketing.checkin', '/admin/ticketing/checkin'),
        ('admin.tourney', None),
        ('admin.tourney.category', '/admin/tourney/categories'),
        ('admin.tourney.tourney', '/admin/tourney/tourneys'),
        ('admin.user', '/admin/users'),
        ('admin.user_badge', '/admin/user_badges'),
        ('admin.webhook', '/admin/webhooks'),
    ]
