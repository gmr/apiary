"""
Profile Model

"""
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Text

from apiary.mappers import Base
from apiary.mappers import mixin


class Profile(Base, mixin.MapperMixin):
    """Profiles allow hardware and software specific overrides for
    Distributions.

    """
    __primary_key__ = 'name'
    __tablename__ = 'system_profiles'

    name = Column(Text, nullable=False, primary_key=True)
    distribution = Column(Text,
                          ForeignKey('distributions.name'),
                          nullable=False)
    parent = Column(Text, ForeignKey('system_profiles.name'), nullable=True)
    kernel_options = Column(Text)

    def __repr__(self):
        """Return the representation of the object

        :rtype: str

        """
        return "<Profile('%s')>" % self.name
