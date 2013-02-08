"""
Distribution Breed Model

"""
from sqlalchemy import Column
from sqlalchemy import Text

from apiary.mappers import Base
from apiary.mappers import mixin


class Breed(Base, mixin.MapperMixin):
    """Distribution breeds specify the top level project or project for a
    distribution such as redhat, debian, etc. This allows for common paths for
    related distributions such as centos and ubuntu.

    """
    __primary_key__ = 'name'
    __tablename__ = 'distribution_breeds'

    name = Column(Text, primary_key=True, nullable=False)

    def __repr__(self):
        """Return the representation of the object

        :rtype: str

        """
        return "<Breed('%s')>" % self.name
