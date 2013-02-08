"""
Web Interface Session Mapper

"""
import datetime
import uuid

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Text

from apiary.types import JSONEncodedValue
from apiary.types import IPAddress
from apiary.types import UUID

from apiary.mappers import Base


class Session(Base):
    """Define the mapper for carrying session data"""
    __tablename__ = 'sessions'

    id = Column(UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    authenticated = Column(Boolean, default=False, nullable=False)
    groups = Column(JSONEncodedValue)
    last_request_at = Column(DateTime, nullable=False,
                             default=datetime.datetime.now())
    last_request_uri = Column(Text, nullable=False)
    profile = Column(JSONEncodedValue)
    remote_ip = Column(IPAddress, nullable=False)
    started_at = Column(DateTime, nullable=False,
                        default=datetime.datetime.now())

    def __repr__(self):
        """Return the representation of the object

        :rtype: str

        """
        return '<Session %s (%s)>' % (self.id, self.remote_ip)
