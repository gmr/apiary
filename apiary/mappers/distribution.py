"""
Distribution related models

"""
from sqlalchemy import func
from sqlalchemy.ext import hybrid
from sqlalchemy import orm
from sqlalchemy.sql.expression import select

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Text

from apiary.mappers import Base
from apiary.mappers import architecture
from apiary.mappers import breed
from apiary.mappers import mixin
from apiary.mappers import profile


class Distribution(Base, mixin.MapperMixin):
    """The top level object for an Operating System to install on systems is
    a Distribution.

    """
    __append__ = ['profile_count']
    __columns__ = ['name', 'version', 'architecture', 'breed', 'profiles']
    __primary_key__ = 'name'
    __tablename__ = 'distributions'

    name = Column(Text, primary_key=True, nullable=False)
    version = Column(Text, nullable=False)
    architecture = Column(Text,
                          ForeignKey(architecture.Architecture.primary_key),
                          nullable=False)
    breed = Column(Text, ForeignKey(breed.Breed.primary_key), nullable=False)
    kernel = Column(Text)
    initrd = Column(Text)
    kernel_options = Column(Text)

    profiles = orm.relationship("Profile")

    def __reprs__(self):
        """Return the representation of the object

        :rtype: str

        """
        return "<Distribution('%s (%s) %s')>" % (self.name,
                                                 self.architecture,
                                                 self.version)

    @hybrid.hybrid_property
    def profile_count(self):
        return len(self.profiles)

    @profile_count.expression
    def profile_count(cls):
        return (select([func.count(profile.Profile.name)]).
                where(profile.Profile.distribution == cls.name).
                label("profile_count"))
