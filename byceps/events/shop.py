"""
byceps.events.shop
~~~~~~~~~~~~~~~~~~

:Copyright: 2014-2023 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from __future__ import annotations

from dataclasses import dataclass

from byceps.events.base import EventUser
from byceps.services.shop.order.models.number import OrderNumber
from byceps.services.shop.order.models.order import OrderID

from .base import _BaseEvent


@dataclass(frozen=True)
class _ShopOrderEvent(_BaseEvent):
    order_id: OrderID
    order_number: OrderNumber
    orderer: EventUser


@dataclass(frozen=True)
class ShopOrderPlacedEvent(_ShopOrderEvent):
    pass


@dataclass(frozen=True)
class ShopOrderCanceledEvent(_ShopOrderEvent):
    pass


@dataclass(frozen=True)
class ShopOrderPaidEvent(_ShopOrderEvent):
    payment_method: str
