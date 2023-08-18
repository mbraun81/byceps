"""
byceps.services.guest_server.models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2014-2023 Jochen Kupperschmidt
:License: Revised BSD (see `LICENSE` file for details)
"""

from __future__ import annotations

from datetime import datetime
import ipaddress
from typing import TYPE_CHECKING

from sqlalchemy.dialects import postgresql


if TYPE_CHECKING:
    hybrid_property = property
else:
    from sqlalchemy.ext.hybrid import hybrid_property

from byceps.database import db
from byceps.typing import PartyID, UserID
from byceps.util.instances import ReprBuilder

from .models import AddressID, IPAddress, ServerID


class DbSetting(db.Model):
    """A party-specific setting for guest servers."""

    __tablename__ = 'guest_server_settings'

    party_id = db.Column(
        db.UnicodeText, db.ForeignKey('parties.id'), primary_key=True
    )
    _netmask = db.Column('netmask', postgresql.INET, nullable=True)
    _gateway = db.Column('gateway', postgresql.INET, nullable=True)
    _dns_server1 = db.Column('dns_server1', postgresql.INET, nullable=True)
    _dns_server2 = db.Column('dns_server2', postgresql.INET, nullable=True)
    domain = db.Column(db.UnicodeText, nullable=True)

    def __init__(self, party_id: PartyID) -> None:
        self.party_id = party_id

    @hybrid_property
    def netmask(self) -> IPAddress | None:
        if not self._netmask:
            return None

        return ipaddress.ip_address(self._netmask)

    @netmask.setter
    def netmask(self, netmask: IPAddress | None) -> None:
        self._netmask = str(netmask) if netmask else None

    @hybrid_property
    def gateway(self) -> IPAddress | None:
        if not self._gateway:
            return None

        return ipaddress.ip_address(self._gateway)

    @gateway.setter
    def gateway(self, ip_address: IPAddress | None) -> None:
        self._gateway = str(ip_address) if ip_address else None

    @hybrid_property
    def dns_server1(self) -> IPAddress | None:
        if not self._dns_server1:
            return None

        return ipaddress.ip_address(self._dns_server1)

    @dns_server1.setter
    def dns_server1(self, ip_address: IPAddress | None) -> None:
        self._dns_server1 = str(ip_address) if ip_address else None

    @hybrid_property
    def dns_server2(self) -> IPAddress | None:
        if not self._dns_server2:
            return None

        return ipaddress.ip_address(self._dns_server2)

    @dns_server2.setter
    def dns_server2(self, ip_address: IPAddress | None) -> None:
        self._dns_server2 = str(ip_address) if ip_address else None

    def __repr__(self) -> str:
        return ReprBuilder(self).add_with_lookup('party_id').build()


class DbServer(db.Model):
    """A guest server."""

    __tablename__ = 'guest_servers'

    id = db.Column(db.Uuid, primary_key=True)
    party_id = db.Column(
        db.UnicodeText, db.ForeignKey('parties.id'), index=True, nullable=False
    )
    created_at = db.Column(db.DateTime, nullable=False)
    creator_id = db.Column(db.Uuid, db.ForeignKey('users.id'), nullable=False)
    owner_id = db.Column(db.Uuid, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.UnicodeText, nullable=True)
    notes_owner = db.Column(db.UnicodeText, nullable=True)
    notes_admin = db.Column(db.UnicodeText, nullable=True)
    approved = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(
        self,
        server_id: ServerID,
        party_id: PartyID,
        created_at: datetime,
        creator_id: UserID,
        owner_id: UserID,
        *,
        description: str | None = None,
        notes_owner: str | None = None,
        notes_admin: str | None = None,
        approved: bool = False,
    ) -> None:
        self.id = server_id
        self.party_id = party_id
        self.created_at = created_at
        self.creator_id = creator_id
        self.owner_id = owner_id
        self.description = description
        self.notes_owner = notes_owner
        self.notes_admin = notes_admin
        self.approved = approved

    def __repr__(self) -> str:
        return ReprBuilder(self).add_with_lookup('id').build()


class DbAddress(db.Model):
    """An guest server's IPv4 address and optional DNS name."""

    __tablename__ = 'guest_server_addresses'

    id = db.Column(db.Uuid, primary_key=True)
    server_id = db.Column(
        db.Uuid, db.ForeignKey('guest_servers.id'), index=True, nullable=False
    )
    server = db.relationship(DbServer, backref='addresses')
    created_at = db.Column(db.DateTime, nullable=False)
    _ip_address = db.Column('ip_address', postgresql.INET, nullable=True)
    hostname = db.Column(db.UnicodeText, nullable=True)
    _netmask = db.Column('netmask', postgresql.INET, nullable=True)
    _gateway = db.Column('gateway', postgresql.INET, nullable=True)

    def __init__(
        self,
        address_id: AddressID,
        server_id: ServerID,
        created_at: datetime,
        *,
        ip_address: IPAddress | None = None,
        hostname: str | None = None,
        netmask: IPAddress | None = None,
        gateway: IPAddress | None = None,
    ) -> None:
        self.id = address_id
        self.server_id = server_id
        self.created_at = created_at
        self.ip_address = ip_address
        self.hostname = hostname
        self.netmask = netmask
        self.gateway = gateway

    @hybrid_property
    def ip_address(self) -> IPAddress | None:
        if not self._ip_address:
            return None

        return ipaddress.ip_address(self._ip_address)

    @ip_address.setter
    def ip_address(self, ip_address: IPAddress | None) -> None:
        self._ip_address = str(ip_address) if ip_address else None

    @hybrid_property
    def netmask(self) -> IPAddress | None:
        if not self._netmask:
            return None

        return ipaddress.ip_address(self._netmask)

    @netmask.setter
    def netmask(self, netmask: IPAddress | None) -> None:
        self._netmask = str(netmask) if netmask else None

    @hybrid_property
    def gateway(self) -> IPAddress | None:
        if not self._gateway:
            return None

        return ipaddress.ip_address(self._gateway)

    @gateway.setter
    def gateway(self, ip_address: IPAddress | None) -> None:
        self._gateway = str(ip_address) if ip_address else None

    def __repr__(self) -> str:
        return ReprBuilder(self).add_with_lookup('id').build()
