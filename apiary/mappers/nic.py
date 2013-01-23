"""
Network Interface Card

"""
import sqlalchemy

from apiary import types
from apiary.mappers import Base
from apiary.mappers import system


class NIC(Base):
    """A network interface card

    """
    __tablename__ = 'system_nics'

    mac_address = sqlalchemy.Column(sqlalchemy.TEXT, primary_key=True,
                                    nullable=False)
    system_fk = sqlalchemy.ForeignKey('%s.id' % system.System.__tablename__)
    system = sqlalchemy.Column(types.UUID, system_fk, nullable=False)
    enabled = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)
    name = sqlalchemy.Column(sqlalchemy.TEXT, nullable=False)
    is_bonded = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)
    bonding_nics = sqlalchemy.Column(sqlalchemy.Enum)
    ip_address = sqlalchemy.Column(sqlalchemy.TEXT)
    netmask = sqlalchemy.Column(sqlalchemy.TEXT)
    gateway = sqlalchemy.Column(sqlalchemy.TEXT)
    dnsname = sqlalchemy.Column(sqlalchemy.TEXT)

    def __repr__(self):
        """Return the representation of the object

        :rtype: str

        """
        return "<NIC System %s Address %s IP %s>" % (self.system,
                                                     self.mac_address,
                                                     self.ip_address)
