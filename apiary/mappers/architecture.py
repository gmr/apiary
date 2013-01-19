"""
Distribution Architecture Model

"""
import sqlalchemy

from apiary.mappers import Base


class Architecture(Base):
    """Distribution Architecture model, used to specify the processor
    architecture (x86_64, i386, etc) for a distribution

    """
    __tablename__ = 'distribution_architectures'

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
