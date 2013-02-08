"""
Distribution Architecture Model

"""
from sqlalchemy import Column
from sqlalchemy import Text

from apiary.mappers import Base
from apiary.mappers import mixin


class Architecture(Base, mixin.MapperMixin):
    """Distribution Architecture model, used to specify the processor
    architecture (x86_64, i386, etc) for a distribution

    """
    __primary_key__ = 'name'
    __tablename__ = 'distribution_architectures'

    name = Column(Text, primary_key=True, nullable=False)

    def __repr__(self):
        """Return the representation of the object

        :rtype: str

        """
        return "<Architecture('%s')>" % self.name
