"""
System Model

"""
import sqlalchemy
import uuid

from apiary.mappers import Base
from apiary.mappers import profile
from apiary import types

class System(Base):
    """Represents a unique system, physical or virtual"""
    __tablename__ = 'systems'
    __columns__ = ['id', 'hostname', 'serial_number', 'provision']

    # Core system configuration
    id = sqlalchemy.Column(types.UUID, primary_key=True,
                           default=uuid.uuid4, nullable=False)
    hostname = sqlalchemy.Column(sqlalchemy.TEXT, nullable=False)
    profile_fk = sqlalchemy.ForeignKey('%s.name' %
                                       profile.Profile.__tablename__)
    profile = sqlalchemy.Column(sqlalchemy.TEXT, profile_fk, nullable=False)
    kernel_options = sqlalchemy.Column(sqlalchemy.TEXT)
    hostname = sqlalchemy.Column(sqlalchemy.TEXT)
    provision = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)

    # Hardware Information
    serial_number = sqlalchemy.Column(sqlalchemy.TEXT)
    manufacturer = sqlalchemy.Column(sqlalchemy.TEXT)
    model = sqlalchemy.Column(sqlalchemy.TEXT)
    cpu_cores = sqlalchemy.Column(sqlalchemy.INTEGER)
    cpu_model = sqlalchemy.Column(sqlalchemy.TEXT)
    ram = sqlalchemy.Column(sqlalchemy.INTEGER)
    nics = sqlalchemy.Column(sqlalchemy.Enum)

    def __repr__(self):
        """Return the representation of the object

        :rtype: str

        """
        return "<System('%s', '%s')>" % (self.hostname, self.id)
