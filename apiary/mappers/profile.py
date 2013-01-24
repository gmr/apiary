"""
Profile Model

"""
import sqlalchemy

from apiary.mappers import Base
from apiary.mappers import distribution
from apiary import types


class Profile(Base):
    """Profiles allow hardware and software specific overrides for
    Distributions.

    """
    __tablename__ = 'system_profiles'

    name = sqlalchemy.Column(sqlalchemy.TEXT, nullable=False, primary_key=True)
    distro_fk = sqlalchemy.ForeignKey('%s.name' %
                                      distribution.Distribution.__tablename__)
    distribution = sqlalchemy.Column(types.TEXT, distro_fk, nullable=False)
    parent = sqlalchemy.Column(sqlalchemy.TEXT,
                               sqlalchemy.ForeignKey('system_profiles.name'),
                               nullable=True)
    kernel_options = sqlalchemy.Column(sqlalchemy.TEXT)

    def __repr__(self):
        """Return the representation of the object

        :rtype: str

        """
        return "<Profile('%s')>" % self.name
