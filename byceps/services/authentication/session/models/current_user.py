"""
byceps.services.authentication.session.models.current_user
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2021 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from dataclasses import dataclass
from enum import Enum
from typing import Set

from .....services.user.transfer.models import User


@dataclass(eq=False, frozen=True)
class CurrentUser(User):
    """The current user, anonymous or logged in."""

    authenticated: bool
    permissions: Set[Enum]

    def __eq__(self, other) -> bool:
        return (other is not None) and (self.id == other.id)
