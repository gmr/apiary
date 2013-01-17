"""
Architecture API related Request Handlers

"""
from apiary.api import base
from apiary.models import architecture
import logging

LOGGER = logging.getLogger(__name__)


class Architecture(base.RequestHandler):
    """API interface for managing architecture data"""

    JSONP_METHOD = 'on_architecture'

    def fetch_architecture(self, kwargs):
        """Get a single architecture from the database.

        :param dict kwargs: Keyword arguments from the request
        :rtype: apiary.models.architecture.Architecture

        """
        name = self.parameter_value('name', kwargs)
        if name:
            return self.new_query(architecture.Architecture).get(name)

    def delete(self, *args, **kwargs):
        """Delete a architecture from the system. Accepts architecture_id as a
        query parameter or in the URI

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        value = self.fetch_architecture(kwargs)
        if not value:
            return self.set_status(404)
        LOGGER.warning('Deleting architecture %s', value.id)
        self.database.delete(value)
        self.database.commit()
        self.set_status(204)

    def get(self, *args, **kwargs):
        """Return the details for a architecture from the system. Accepts
        architecture_id as a query parameter or in the URI

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        value = self.fetch_architecture(kwargs)
        if not value:
            return self.set_status(404)
        self.write_mapping(value)

    def post(self, *args, **kwargs):
        """Insert or update a architecture in the system.

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        value = self.fetch_architecture(kwargs)

        # Insert
        if not value:
            distro = architecture.Architecture()
            self.assign_attributes(distro, kwargs)
            self.database.add(distro)
            self.database.commit()
            LOGGER.info('Added new architecture: %r', distro)
            return self.set_status(201)

        # Update
        self.assign_attributes(value, kwargs)
        self.database.update(value)
        self.database.commit()
        LOGGER.info('Updated architecture: %r', value)
        return self.set_status(204)


class Architectures(base.RequestHandler):
    """API interface for fetching a list of architectures"""

    JSONP_METHOD = 'on_architectures'

    def get(self, *args, **kwargs):
        """Return a list of definitions from the system. Optional query
        parameters include:

        - limit: Limit the quantity of rows
        - offset: The starting offset in the list to return, use with limit
        - filter: Filter the list by the specified criteria

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        self.write_query_results(architecture.Architecture)
