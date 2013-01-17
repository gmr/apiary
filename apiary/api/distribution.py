"""
API Distribution related Request Handlers

"""
from apiary.api import base
from apiary.models import distribution
import logging

LOGGER = logging.getLogger(__name__)


class Distribution(base.RequestHandler):
    """API interface for managing distribution data"""

    JSONP_METHOD = 'on_distribution'

    def fetch_distribution(self, kwargs):
        """Get a single distribution from the database.

        :param dict kwargs: Keyword arguments from the request
        :rtype: apiary.models.distribution.Distribution

        """
        distribution_id = self.parameter_value('id', kwargs)
        if distribution_id:
            return self.query(distribution.Distribution).get(distribution_id)

    def delete(self, *args, **kwargs):
        """Delete a distribution from the system. Accepts distribution_id as a
        query parameter or in the URI

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        value = self.fetch_distribution(kwargs)
        if not value:
            return self.set_status(404)
        LOGGER.warning('Deleting distribution %s', value.id)
        self.database.delete(value)
        self.database.commit()
        self.set_status(204)

    def get(self, *args, **kwargs):
        """Return the details for a distribution from the system. Accepts
        distribution_id as a query parameter or in the URI

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        value = self.fetch_distribution(kwargs)
        if not value:
            return self.set_status(404)
        self.write_mapping(value)

    def post(self, *args, **kwargs):
        """Insert or update a distribution in the system.

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        value = self.fetch_distribution(kwargs)

        # Insert
        if not value:
            distro = distribution.Distribution()
            self.assign_attributes(distro, kwargs)
            self.database.add(distro)
            self.database.commit()
            LOGGER.info('Added new distribution: %r', distro)
            return self.set_status(201)

        # Update
        self.assign_attributes(value, kwargs)
        self.database.update(value)
        self.database.commit()
        LOGGER.info('Updated distribution: %r', value)
        return self.set_status(204)


class Distributions(base.RequestHandler):
    """API interface for fetching a list of distributions"""

    JSONP_METHOD = 'on_distributions'

    def get(self, *args, **kwargs):
        """Return a list of definitions from the system. Optional query
        parameters include:

        - limit: Limit the quantity of rows
        - offset: The starting offset in the list to return, use with limit
        - filter: Filter the list by the specified criteria

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        self.write_query_results(distribution.Distribution)
