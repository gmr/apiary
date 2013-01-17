"""
API Distribution related Request Handlers

"""
from apiary.api import base
from apiary.models import distro
import logging

LOGGER = logging.getLogger(__name__)


class Distribution(base.RequestHandler):

    JSONP_METHOD = 'on_distribution'

    def fetch_distribution(self, kwargs):
        distribution_id = self.parameter_value('id', kwargs)
        if distribution_id:
            return self.database.query(distro.Distribution).get(distribution_id)

    def delete(self, *args, **kwargs):
        value = self.fetch_distribution(kwargs)
        if not value:
            return self.set_status(404)
        LOGGER.info('Deleting distribution %s', value.id)
        self.database.delete(value)
        self.database.commit()
        self.set_status(204)

    def get(self, *args, **kwargs):
        value = self.fetch_distribution(kwargs)
        if not value:
            return self.set_status(404)
        self.write_mapping(value)

    def post(self, *args, **kwargs):
        value = self.fetch_distribution(kwargs)

        # Insert
        if not value:
            distribution = distro.Distribution()
            self.assign_attributes(distribution, kwargs)
            self.database.add(distribution)
            self.database.commit()
            return self.set_status(201)

        # Update
        self.assign_attributes(value, kwargs)
        self.database.update(value)
        self.database.commit()
        return self.set_status(204)


class Distributions(base.RequestHandler):

    JSONP_METHOD = 'on_distributions'

    def get(self, *args, **kwargs):
        self.write_query_results(distro.Distribution)
