"""
Base Mixin Class for Dynamic Attributes

"""
from sqlalchemy.ext import declarative
import re

FIRST_PASS = re.compile(r'(.)([A-Z][a-z]+)')
LAST_PASS = re.compile(r'([a-z0-9])([A-Z])')


class MapperMixin(object):

    __columns__ = []
    __primary_key__ = None
    __tablename__ = None

    @declarative.declared_attr
    def primary_key(cls):
        return '%s.%s' % (cls.__tablename__, cls.__primary_key__)

    @declarative.declared_attr
    def table_name(cls):
        return cls.__tablename__


class AutoNameMapperMixin(MapperMixin):

    @declarative.declared_attr
    def __tablename__(cls):
        temp = FIRST_PASS.sub(r'\1_\2', cls.__name__)
        return '%s' % LAST_PASS.sub( r'\1_\2', temp).lower()
