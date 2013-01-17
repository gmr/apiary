"""
Profile Model

"""
import sqlalchemy

from apiary.models import distribution
from apiary.models import base
from apiary import types


class Profile(base.Base):
    """Profiles allow hardware and software specific overrides for
    Distributions.

    """
    __tablename__ = 'system_profiles'

    name = sqlalchemy.Column(sqlalchemy.TEXT, nullable=False, primary_key=True)
    distro_fk = sqlalchemy.ForeignKey('%s.id' %
                                      distribution.Distribution.__tablename__)
    distribution = sqlalchemy.Column(types.UUID, distro_fk, nullable=False)
    kernel_options = sqlalchemy.Column(sqlalchemy.TEXT)

    def __repr__(self):
        """Return the representation of the object

        :rtype: str

        """
        return "<Profile('%s')>" % self.name
