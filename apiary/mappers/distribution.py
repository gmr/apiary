"""
Distribution related models

"""
import sqlalchemy
from sqlalchemy.ext import hybrid
from sqlalchemy import func
from sqlalchemy import orm
import uuid

from apiary.mappers import Base
from apiary.mappers import architecture
from apiary.mappers import breed
from apiary.mappers import profile
from apiary.mappers import system
from apiary import types


class Distribution(Base):
    """The top level object for an Operating System to install on systems is
    a Distribution.

    """
    __tablename__ = 'distributions'
    __columns__ = ['name', 'version', 'architecture', 'breed', 'profiles']
    __append__ = ['profile_count']

    name = sqlalchemy.Column(sqlalchemy.TEXT, primary_key=True, nullable=False)
    version = sqlalchemy.Column(sqlalchemy.TEXT, nullable=False)
    arch_fk = sqlalchemy.ForeignKey('%s.name' %
                                    architecture.Architecture.__tablename__)
    architecture = sqlalchemy.Column(sqlalchemy.TEXT, arch_fk)
    breed_fk = sqlalchemy.ForeignKey('%s.name' % breed.Breed.__tablename__)
    breed = sqlalchemy.Column(sqlalchemy.TEXT, breed_fk)
    kernel = sqlalchemy.Column(sqlalchemy.TEXT)
    initrd = sqlalchemy.Column(sqlalchemy.TEXT)
    kernel_options = sqlalchemy.Column(sqlalchemy.TEXT)

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
        return (sqlalchemy.select([func.count(profile.Profile.name)]).
                sqlalchemy.where(profile.Profile.distribution == cls.name).
                sqlalchemy.label("profile_count"))
