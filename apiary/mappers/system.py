"""
System Model

"""
from sqlalchemy import orm
import uuid

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import Text

from apiary.types import UUID

from apiary.mappers import Base
from apiary.mappers import mixin
from apiary.mappers import profile


class System(Base, mixin.MapperMixin):
    """Represents a unique system, physical or virtual"""
    __columns__ = ['id', 'hostname', 'serial_number', 'provision']
    __primary_key__ = 'id'
    __tablename__ = 'systems'

    # Core system configuration
    id = Column(UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    hostname = Column(Text, nullable=False, unique=True)
    profile = Column(Text, ForeignKey(profile.Profile.primary_key),
                     nullable=False)
    provision = Column(Boolean, default=False)
    kernel_options = Column(Text, nullable=True)

    # Hardware Information
    serial_number = Column(Text, nullable=True)
    manufacturer = Column(Text, nullable=True)
    model = Column(Text, nullable=True)
    cpu_cores = Column(Integer, nullable=True)
    cpu_model = Column(Text, nullable=True)
    ram = Column(Integer, nullable=True)

    nics = orm.relationship('NICAssignment',
                            backref='system_id',
                            cascade='all, delete, delete-orphan')

    def __repr__(self):
        """Return the representation of the object

        :rtype: str

        """
        return "<System %s>" % self.id
