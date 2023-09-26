"""
byceps.services.verification_token.models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2014-2023 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from byceps.services.user.models.user import User


Purpose = Enum(
    'Purpose',
    [
        'consent',
        'email_address_change',
        'email_address_confirmation',
        'password_reset',
    ],
)


@dataclass(frozen=True)
class _BaseVerificationToken:
    token: str
    created_at: datetime
    user: User


@dataclass(frozen=True)
class VerificationToken(_BaseVerificationToken):
    purpose: Purpose
    data: dict[str, str]


@dataclass(frozen=True)
class ConsentToken(_BaseVerificationToken):
    pass


@dataclass(frozen=True)
class EmailAddressChangeToken(_BaseVerificationToken):
    new_email_address: str


@dataclass(frozen=True)
class EmailAddressConfirmationToken(_BaseVerificationToken):
    email_address: str
