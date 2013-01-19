"""
Breed API related Request Handlers

"""
import logging

from apiary.mappers import breed
from apiary import web

LOGGER = logging.getLogger(__name__)


class Breed(web.APIRequestHandler):
    """API interface for managing breed data"""

    JSONP_METHOD = 'on_breed'

    def fetch_breed(self, kwargs):
        """Get a single breed from the database.

        :param dict kwargs: Keyword arguments from the request
        :rtype: apiary.mappers.breed.Breed

        """
        name = self.parameter_value('name', kwargs)
        if name:
            return self.new_query(breed.Breed).get(name)

    def delete(self, *args, **kwargs):
        """Delete a breed from the system. Accepts breed_id as a
        query parameter or in the URI

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        value = self.fetch_breed(kwargs)
        if not value:
            return self.set_status(404)
        LOGGER.warning('Deleting breed %s', value.id)
        self.database.delete(value)
        self.database.commit()
        self.set_status(204)

    def get(self, *args, **kwargs):
        """Return the details for a breed from the system. Accepts
        breed_id as a query parameter or in the URI

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        value = self.fetch_breed(kwargs)
        if not value:
            return self.set_status(404)
        self.write_mapping(value)

    def post(self, *args, **kwargs):
        """Insert or update a breed in the system.

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        value = self.fetch_breed(kwargs)

        # Insert
        if not value:
            distro = breed.Breed()
            self.assign_attributes(distro, kwargs)
            self.database.add(distro)
            self.database.commit()
            LOGGER.info('Added new breed: %r', distro)
            return self.set_status(201)

        # Update
        self.assign_attributes(value, kwargs)
        self.database.merge(value)
        self.database.commit()
        LOGGER.info('Updated breed: %r', value)
        return self.set_status(204)


class Breeds(web.APIRequestHandler):
    """API interface for fetching a list of breeds"""

    JSONP_METHOD = 'on_breeds'

    def get(self, *args, **kwargs):
        """Return a list of definitions from the system. Optional query
        parameters include:

        - limit: Limit the quantity of rows
        - offset: The starting offset in the list to return, use with limit
        - filter: Filter the list by the specified criteria

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        self.write_query_results(breed.Breed)
