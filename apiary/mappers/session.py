"""
Web Interface Session Mapper

"""
import datetime
import sqlalchemy
import uuid

from apiary.mappers import Base
from apiary import types


class Session(Base):
    """Define the mapper for carrying session data"""
    __tablename__ = 'sessions'

    id = sqlalchemy.Column(types.UUID, primary_key=True, nullable=False,
                           default=uuid.uuid4)
    authenticated = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False,
                                      nullable=False)
    groups = sqlalchemy.Column(types.JSONEncodedDict)
    last_request_at = sqlalchemy.Column(sqlalchemy.DATETIME, nullable=False,
                                        default=datetime.datetime.now())
    last_request_uri = sqlalchemy.Column(sqlalchemy.TEXT, nullable=False)
    profile = sqlalchemy.Column(types.JSONEncodedDict)
    remote_ip = sqlalchemy.Column(sqlalchemy.TEXT, nullable=False)
    started_at = sqlalchemy.Column(sqlalchemy.DATETIME, nullable=False,
                                   default=datetime.datetime.now())

    def __repr__(self):
        """Return the representation of the object

        :rtype: str

        """
        return "<Session %s>" % self.id
