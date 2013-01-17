"""
Definition of additional SQLAlchemy types

"""
from sqlalchemy.dialects import mysql
from sqlalchemy.dialects import postgres
from sqlalchemy import types
import uuid

import logging


LOGGER = logging.getLogger(__name__)

class UUID(types.TypeDecorator):
    """UUID column type for SQLAlchemy based on SQLAlchemy doc examples for GUID
    and an example from Tom Willis for MySQL:

    http://blog.sadphaeton.com/2009/01/19/sqlalchemy-recipeuuid-column.html

    """
    impl = types.CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'mysql':
            return dialect.type_descriptor(mysql.MSBinary)
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(postgres.UUID())
        else:
            return dialect.type_descriptor(types.CHAR(32))

    def process_bind_param(self, value, dialect=None):
        if not value:
            return None
        if isinstance(value, uuid.UUID):
            if dialect.name == 'mysql':
                return value.bytes
            elif dialect.name == 'postgresql':
                return str(value)
            else:
                return str(value)
        return str(uuid.UUID('urn:uuid:%s' % value))

    def process_result_value(self, value, dialect=None):
        if value:
            return uuid.UUID(value)
        return None

    def is_mutable(self):
        return False
