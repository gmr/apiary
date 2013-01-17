"""
Distribution related models

"""
import sqlalchemy
import uuid

from apiary.models import architecture
from apiary.models import base
from apiary.models import breed
from apiary import types


class Distribution(base.Base):
    """The top level object for an Operating System to install on systems is
    a Distribution.

    """
    __tablename__ = 'distributions'

    id = sqlalchemy.Column(types.UUID, primary_key=True,
                           default=uuid.uuid4, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.TEXT, nullable=False)
    version = sqlalchemy.Column(sqlalchemy.TEXT, nullable=False)
    arch_fk = sqlalchemy.ForeignKey('%s.name' %
                                    architecture.Architecture.__tablename__)
    architecture = sqlalchemy.Column(sqlalchemy.TEXT, arch_fk)
    breed_fk = sqlalchemy.ForeignKey('%s.name' % breed.Breed.__tablename__)
    breed = sqlalchemy.Column(sqlalchemy.TEXT, breed_fk)
    kernel = sqlalchemy.Column(sqlalchemy.TEXT)
    initrd = sqlalchemy.Column(sqlalchemy.TEXT)
    kernel_options = sqlalchemy.Column(sqlalchemy.TEXT)

    def __repr__(self):
        """Return the representation of the object

        :rtype: str

        """
        return "<Distribution('%s', '%s (%s) %s')>" % (self.id,
                                                       self.name,
                                                       self.architecture,
                                                       self.version)
