"""
API NIC related Request Handlers

"""
import logging

from apiary.mappers import nic
from apiary import web

LOGGER = logging.getLogger(__name__)


class NIC(web.APIRequestHandler):
    """API interface for managing nic data"""

    JSONP_METHOD = 'on_nic'

    def fetch_nic(self, kwargs):
        """Get a single nic from the database.

        :param dict kwargs: Keyword arguments from the request
        :rtype: apiary.mappers.nic.NIC

        """
        mac_addr = self.parameter_value('mac_address', kwargs)
        if mac_addr:
            return self.new_query(nic.NIC).get(mac_addr)

    def delete(self, *args, **kwargs):
        """Delete a nic from the nic. Accepts nic_id as a
        query parameter or in the URI

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        value = self.fetch_nic(kwargs)
        if not value:
            return self.set_status(404)
        LOGGER.warning('Deleting nic %s', value.id)
        self.database.delete(value)
        self.database.commit()
        self.set_status(204)

    def get(self, *args, **kwargs):
        """Return the details for a nic from the nic. Accepts
        nic_id as a query parameter or in the URI

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        value = self.fetch_nic(kwargs)
        if not value:
            return self.set_status(404)
        self.write_mapping(value)

    def post(self, *args, **kwargs):
        """Insert or update a nic in the nic.

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        value = self.fetch_nic(kwargs)

        # Insert
        if not value:
            distro = nic.NIC()
            self.assign_attributes(distro, kwargs)
            self.database.add(distro)
            self.database.commit()
            LOGGER.info('Added new nic: %r', distro)
            return self.set_status(201)

        # Update
        self.assign_attributes(value, kwargs)
        self.database.merge(value)
        self.database.commit()
        LOGGER.info('Updated nic: %r', value)
        return self.set_status(204)


class NICs(web.APIRequestHandler):
    """API interface for fetching a list of nics"""

    JSONP_METHOD = 'on_nics'

    def get(self, *args, **kwargs):
        """Return a list of definitions from the nic. Optional query
        parameters include:

        - limit: Limit the quantity of rows
        - offset: The starting offset in the list to return, use with limit
        - filter: Filter the list by the specified criteria

        :param list args: Positional arguments
        :param dict kwargs: Keyword arguments

        """
        self.write_query_results(nic.NIC)
