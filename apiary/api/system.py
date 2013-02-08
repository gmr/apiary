"""
API System related Request Handlers

"""
import logging

from apiary.mappers import nic
from apiary.mappers import system
from apiary import web

LOGGER = logging.getLogger(__name__)


class System(web.APIRequestHandler):
    """API interface for managing system data"""

    JSONP_METHOD = 'on_system'

    def fetch_system(self, kwargs):
        """Get a single system from the database.

        :param dict kwargs: Keyword arguments from the request
        :rtype: apiary.mappers.system.System

        """
        system_id = self.parameter_value('id', kwargs)
        if system_id:
            return self.new_query(system.System).get(system_id)

    def delete(self, *args, **kwargs):
        """Delete a system from the system. Accepts system_id as a
        query parameter or in the URI

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        value = self.fetch_system(kwargs)
        if not value:
            return self.set_status(404)
        LOGGER.warning('Deleting system %s', value.id)
        self.database.delete(value)
        self.database.commit()
        self.set_status(204)

    def get(self, *args, **kwargs):
        """Return the details for a system from the system. Accepts
        system_id as a query parameter or in the URI

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        value = self.fetch_system(kwargs)
        if not value:
            return self.set_status(404)
        self.write_mapping(value)

    def post(self, *args, **kwargs):
        """Insert or update a system in the system.

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        value = self.fetch_system(kwargs)

        # Insert
        if not value:
            distro = system.System()
            self.assign_attributes(distro, kwargs)
            self.database.add(distro)
            self.database.commit()
            LOGGER.info('Added new system: %r', distro)
            return self.set_status(201)

        # Update
        self.assign_attributes(value, kwargs)
        self.database.merge(value)
        self.database.commit()
        LOGGER.info('Updated system: %r', value)
        return self.set_status(204)


class Systems(web.APIRequestHandler):
    """API interface for fetching a list of systems"""

    JSONP_METHOD = 'on_systems'

    def get(self, *args, **kwargs):
        """Return a list of definitions from the system. Optional query
        parameters include:

        - limit: Limit the quantity of rows
        - offset: The starting offset in the list to return, use with limit
        - filter: Filter the list by the specified criteria

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        self.write_query_results(system.System)
