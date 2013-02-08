"""
Network Interface Card

"""
from sqlalchemy import orm
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Text

from apiary.types import IPv4Address
from apiary.types import IPv6Address
from apiary.types import MacAddress
from apiary.types import UUID
from apiary.types import JSONEncodedValue

from apiary.mappers import Base
from apiary.mappers import mixin
from apiary.mappers import system


class NIC(Base, mixin.MapperMixin):
    """Define the attributes and use of a network interface card"""
    __primary_key__ = 'mac_address'
    __tablename__ = 'system_nic'

    mac_address = Column(MacAddress, primary_key=True)
    name = Column(Text, nullable=False)
    is_enabled = Column(Boolean, nullable=False, default=False)
    is_bonded = Column(Boolean, nullable=False, default=False)
    bond = Column(JSONEncodedValue, nullable=True)
    dns_name = Column(Text, nullable=True, unique=True)
    ipv4_address = Column(IPv4Address, nullable=True)
    ipv4_netmask = Column(IPv4Address, nullable=True)
    ipv4_gateway = Column(IPv4Address, nullable=True)
    ipv6_address = Column(IPv6Address, nullable=True)
    ipv6_gateway = Column(IPv6Address, nullable=True)
    system_id = orm.relationship('NICAssignment',
                                 backref='mac_address',
                                 cascade='all, delete')

    def __repr__(self):
        """Return the representation of the object

        :rtype: str

        """
        return '<NIC %s>' % self.mac_address


class NICAssignment(Base, mixin.MapperMixin):
    """A mapping of Systems to Network Interface Cards"""
    __tablename__ = 'system_nic_assignments'

    system = Column('system_id',
                    UUID,
                    ForeignKey(system.System.primary_key),
                    primary_key=True)
    nic = Column('nic_id',
                 MacAddress,
                 ForeignKey(NIC.primary_key),
                 primary_key=True)

    def __repr__(self):
        """Return the representation of the object

        :rtype: str

        """
        return '<NICAssignment %s to %s>' % (self.nic, self.system)
