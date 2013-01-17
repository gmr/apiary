"""
Distribution related models

"""
import sqlalchemy
import uuid

from apiary.models import base
from apiary import types


class Architecture(base.Base):
    """Distribution Architecture model, used to specify the processor
    architecture (x86_64, i386, etc) for a distribution

    """
    __tablename__ = 'distro_architectures'

    name = sqlalchemy.Column(sqlalchemy.TEXT, primary_key=True, nullable=False)

    def __init__(self, name=None):
        """Create a new instance of the Architecture class passing in the
        architecture name.

        :param str name: The name of the architecture ('x86_64', 'i386' etc)

        """
        self.name = name

    def __repr__(self):
        """Return the representation of the object

        :rtype: str

        """
        return "<Architecture('%s')>" % self.name


class Breed(base.Base):
    """Distribution breeds specify the top level project or project for a
    distribution such as redhat, debian, etc. This allows for common paths for
    related distributions such as centos and ubuntu.

    """
    __tablename__ = 'distro_breeds'

    name = sqlalchemy.Column(sqlalchemy.TEXT, primary_key=True, nullable=False)

    def __init__(self, name):
        """Create a new instance of the Breed class, passing in the name of the
        Breed.

        :param str name: The name of the breed (redhat, debian, etc)

        """
        self.name = name

    def __repr__(self):
        """Return the representation of the object

        :rtype: str

        """
        return "<Breed('%s')>" % self.name


class Distribution(base.Base):
    """The top level object for an Operating System to install on systems is
    a Distribution.

    """
    __tablename__ = 'distributions'

    id = sqlalchemy.Column(types.UUID, primary_key=True,
                           default=uuid.uuid4, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.TEXT, nullable=False)
    version = sqlalchemy.Column(sqlalchemy.TEXT, nullable=False)
    arch_fk = sqlalchemy.ForeignKey('%s.name' % Architecture.__tablename__)
    architecture = sqlalchemy.Column(sqlalchemy.TEXT, arch_fk)
    breed_fk = sqlalchemy.ForeignKey('%s.name' % Breed.__tablename__)
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
