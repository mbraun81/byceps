"""
byceps.blueprints.site.seating.service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2021 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from __future__ import annotations
from dataclasses import dataclass
from itertools import chain
from typing import Iterator, Optional, Iterable

from ....services.seating.dbmodels.seat import Seat as DbSeat
from ....services.seating.transfer.models import Seat
from ....services.ticketing.dbmodels.ticket import Ticket as DbTicket
from ....services.ticketing import ticket_service
from ....services.ticketing.transfer.models import TicketCode, TicketID
from ....services.user import service as user_service
from ....services.user.transfer.models import User
from ....typing import UserID


@dataclass(frozen=True)
class ManagedTicket:
    id: TicketID
    code: TicketCode
    category_label: str
    user: Optional[User]
    occupied_seat_label: Optional[str]


def get_users(
    seats: Iterable[DbSeat], managed_tickets: Iterable[DbTicket]
) -> dict[UserID, User]:
    seat_tickets = _get_seat_tickets(seats)
    tickets = chain(seat_tickets, managed_tickets)

    return _get_ticket_users_by_id(tickets)


def _get_seat_tickets(seats: Iterable[DbSeat]) -> Iterator[DbTicket]:
    for seat in seats:
        ticket = seat.occupied_by_ticket
        if (ticket is not None) and (ticket.used_by_id is not None):
            yield ticket


def _get_ticket_users_by_id(tickets: Iterable[DbTicket]) -> dict[UserID, User]:
    user_ids = set(_get_ticket_user_ids(tickets))
    users = user_service.get_users(user_ids, include_avatars=True)
    return user_service.index_users_by_id(users)


def _get_ticket_user_ids(tickets: Iterable[DbTicket]) -> Iterator[UserID]:
    for ticket in tickets:
        user_id = ticket.used_by_id
        if user_id is not None:
            yield user_id


def get_seats_and_tickets(
    seats: Iterable[DbSeat], users_by_id: dict[UserID, User]
) -> Iterator[tuple[Seat, Optional[ManagedTicket]]]:
    for seat in seats:
        seat_dto = Seat(
            seat.id,
            seat.coord_x,
            seat.coord_y,
            seat.category_id,
            seat.label,
            seat.type_,
        )

        managed_ticket = _get_ticket_managed_by_seat(seat, users_by_id)

        yield seat_dto, managed_ticket


def _get_ticket_managed_by_seat(
    seat: DbSeat, users_by_id: dict[UserID, User]
) -> Optional[ManagedTicket]:
    if ticket_service.find_ticket_occupying_seat(seat.id) is None:
        return None

    ticket = seat.occupied_by_ticket
    user = _find_ticket_user(ticket, users_by_id)

    return ManagedTicket(
        ticket.id, ticket.code, ticket.category.title, user, None
    )


def get_managed_tickets(
    managed_tickets: Iterable[DbTicket], users_by_id: dict[UserID, User]
) -> Iterator[ManagedTicket]:
    for ticket in managed_tickets:
        user = _find_ticket_user(ticket, users_by_id)

        if ticket.occupied_seat_id is not None:
            seat_label = ticket.occupied_seat.label
        else:
            seat_label = None

        yield ManagedTicket(
            ticket.id, ticket.code, ticket.category.title, user, seat_label
        )


def _find_ticket_user(
    ticket: DbTicket, users_by_id: dict[UserID, User]
) -> Optional[User]:
    if ticket.used_by_id is None:
        return None

    return users_by_id[ticket.used_by_id]
