"""
Distribution Breed Model

"""
import sqlalchemy

from apiary.mappers import Base


class Breed(Base):
    """Distribution breeds specify the top level project or project for a
    distribution such as redhat, debian, etc. This allows for common paths for
    related distributions such as centos and ubuntu.

    """
    __tablename__ = 'distribution_breeds'

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
