"""
byceps.permissions.seating
~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2021 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from ..util.authorization import create_permission_enum


SeatingPermission = create_permission_enum(
    'seating',
    [
        'administrate',
        'view',
    ],
)