"""
Definition of additional SQLAlchemy types

"""
import json
import logging
from sqlalchemy.dialects import mysql
from sqlalchemy.dialects import postgres
from sqlalchemy import types
import ipaddr
import re
import uuid

LOGGER = logging.getLogger(__name__)


def is_ipv4_address(value):
    try:
        ipaddr.IPv4Address(value)
    except ipaddr.AddressValueError:
        return False
    return True


def is_ipv6_address(value):
    try:
        ipaddr.IPv6Address(value)
    except ipaddr.AddressValueError:
        return False
    return True


class IPAddress(types.TypeDecorator):
    """Abstract the IP address so it uses PostgreSQL's inet type or Text"""
    impl = types.TEXT

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(postgres.INET())
        return dialect.type_descriptor(types.CHAR(45))

    def process_bind_param(self, value, dialect):
        if value and not is_ipv4_address(value) and not is_ipv6_address(value):
            raise ValueError('Could not validate IPv4 or IPv6 format: %s',
                             value)
        return value


class IPv4Address(types.TypeDecorator):
    """Abstract the IP address so it uses PostgreSQL's inet type or Text"""
    impl = types.TEXT

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(postgres.INET())
        return dialect.type_descriptor(types.CHAR(15))

    def process_bind_param(self, value, dialect):
        if value and not is_ipv4_address(value):
            raise ValueError('Could not validate IPv4 format: %s', value)
        return value


class IPv6Address(types.TypeDecorator):
    """Abstract the IP address so it uses PostgreSQL's inet type or Text"""
    impl = types.TEXT

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(postgres.INET())
        return dialect.type_descriptor(types.CHAR(45))

    def process_bind_param(self, value, dialect):
        if value and not is_ipv6_address(value):
            raise ValueError('Could not validate IPv6 format: %s', value)
        return value


class MacAddress(types.TypeDecorator):
    """Abstract the IP address so it uses PostgreSQL's macaddr type or Text"""
    impl = types.TEXT

    PATTERN = re.compile(r'^([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$')

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(postgres.MACADDR())
        return dialect.type_descriptor(types.CHAR(17))

    def process_bind_param(self, value, dialect):
        if value and not self.PATTERN.match(value):
            raise ValueError('Could not validate MAC Address format: %s', value)
        return value


class JSONEncodedValue(types.TypeDecorator):
    """Represents an immutable structure as a json-encoded string from
    SQLAlchemy doc example

    Usage::

        JSONEncodedValue()

    """

    impl = types.TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class UUID(types.TypeDecorator):
    """UUID column type for SQLAlchemy based on SQLAlchemy doc examples for GUID
    and an example from Tom Willis for MySQL:

    http://blog.sadphaeton.com/2009/01/19/sqlalchemy-recipeuuid-column.html

    """
    impl = types.TEXT

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
