"""
Base API Class

"""
from lxml import etree
import json
import logging
import msgpack
import uuid
from tornado import web

LOGGER = logging.getLogger(__name__)

CONTENT_TYPE = 'Content-Type'
HTML = 'html'
JSONP = 'jsonp'
MSGPACK = 'msgpack'
XML = 'xml'

MIME_TYPES = {JSONP: 'application/javascript',
              HTML: 'text/html',
              MSGPACK: 'application/x-msgpack',
              XML: 'text/xml'}


class RequestHandler(web.RequestHandler):
    """Generic base RequestHandler for the RESTful API set that minimizes the
    duplicate functionality across all the APIs. This RequestHandler will send
    different types of output for the request based upon the Accept header and
    will take SQLAlchemy models/mappings and extract the data out.

    """
    JSONP_METHOD = 'on_jsonp'

    def initialize(self):
        self.database = self.application.database

    @property
    def accept_header(self):
        """Return a list of mime types from the accept header as a list of
        strings.

        :rtype: list

        """
        return self.request.headers.get('Accept').split(';')[0].split(',')

    def assign_attributes(self, mapping, kwargs):
        """Assign values passed in via either a GET/POST values or via URI
        parsing to a mapping object.

        :param apiary.models.base.Base mapping: The mapping object
        :param dict kwargs: kwargs passed into the method

        """
        for key in mapping.__table__.columns.keys():
            setattr(mapping, key, self.parameter_value(key, kwargs))

    def generate_multi_item_etree(self, value_in):
        """Generate an etree.Element tree for a dictionary containing mapping
        items in them.

        :param dict value_in: The internal multi-mapping item data structure
        :rtype: lxml.etree.Element

        """
        root = etree.Element('%ss' % value_in['values'][0].__class__.__name__)
        for key in ['filter', 'limit', 'offset']:
            node = etree.Element(key)
            node.text = str(value_in.get(key))
            root.append(node)
        values = etree.Element('values')
        for row in value_in['values']:
            values.append(self.generate_item_etree(row))
        root.append(values)
        return root

    def generate_item_etree(self, value_in):
        """Generate an etree.Element tree for the item passed in

        :param apiary.models.base.Base mapping: The mapping item
        :rtype: lxml.etree.Element

        """
        root = etree.Element(value_in.__class__.__name__)
        for key in value_in.__table__.columns.keys():
            value = getattr(value_in, key)
            if isinstance(value, uuid.UUID):
                value = str(value)
            node = etree.Element(key)
            node.text = value
            root.append(node)
        return root

    def generate_xml(self, value_in):
        """Generate an XML document from the value passed in. if the value
        passed in is a dictionary, it contains multiple items, otherwise it
        contains only one.

        :param apiary.models.base.Base|dict: The item or a multi-item dict
        :rtype: str

        """
        if isinstance(value_in, dict):
            root = self.generate_multi_item_etree(value_in)
        else:
            root = self.generate_item_etree(value_in)
        return etree.tostring(root, pretty_print=True)

    def normalize_mapping_list(self, values_in):
        """Turn a list of mappings into a list of dictionaries representing the
        mappings.

        :param list values_in: The list of mappings
        :rtype: list

        """
        values_out = list()
        for value in values_in:
            values_out.append(self.normalize_mapping(value))
        return values_out

    def normalize_mapping(self, value_in):
        """Turn a mapping object into a dict representation of it

        :param apiary.models.base.Base value_in: The mapping object
        :rtype: dict

        """
        value_out = dict()
        for key in value_in.__table__.columns.keys():
            value = getattr(value_in, key)
            if isinstance(value, uuid.UUID):
                value = str(value)
            value_out[key] = value
        return value_out

    def parameter_value(self, key, kwargs):
        """Get the request value for the specified key by first checking kwargs
        from the URI parsing and then falling back to query string values.

        :param str key: The key to fetch the value for
        :param dict kwargs: KWargs from the request
        :rtype: basestring|int|None

        """
        return kwargs.get(key, self.get_argument(key, None))

    def query(self, mapping, limit=None, offset=None, filter=None):
        """Create and execute a query for the mapping type, applying the limit,
        offset and filter if specified.


        :param apiary.models.base.Base value_in: The mapping class to query for
        :param int limit: Number of rows to limit to (optional)
        :param int offset: The row offset (optional)
        :param str filter: The filter to reply
        :rtype: sqlalchemy.orm.query.Query

        """
        query = self.database.query(mapping)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        if filter:
            filter = query.filter(filter)
        return query.all()

    def normalize(self, value):
        """Take the inbound value and normalize the values returning a python
        dict instead of whatever mapping related type was passed in.

        :param apiary.models.base.Base|dict value: The value to normalize
        :rtype: dict

        """
        if isinstance(value, dict):
            value['values'] = self.normalize_mapping_list(value['values'])
        else:
            value = self.normalize_mapping(value)
        return value

    def new_query(self, mapping):
        """Create a SQLAlchemy Query object for the given mapping

        :param apiary.models.base.Base mapping: The mapping to query
        :rtype: sqlalchemy.query.Query

        """
        return self.database.query(mapping)

    def restful_write(self, value):
        """Handle the outbound writing for the request, applying logic against
        the Accept header to decide how the value should be returned.

        :param apiary.models.base.Base|list value: The value to send

        """
        accept = self.accept_header
        LOGGER.debug('Accept headers: %r', accept)

        # HTML
        if  MIME_TYPES[HTML] in accept:
            self.set_header(CONTENT_TYPE, MIME_TYPES[HTML])
            if isinstance(value, dict):
                return self.render('api/table.html', values=value)
            return self.render('api/item.html', value=value)

        # JSON-P
        if MIME_TYPES[JSONP] in accept:
            method_name = self.get_argument('callback', self.JSONP_METHOD)
            self.set_header(CONTENT_TYPE, MIME_TYPES[JSONP])
            return self.finish('%s(%s)' % (method_name,
                                           json.dumps(self.normalize(value),
                                                      ensure_ascii=False)))

        # MsgPack
        if MIME_TYPES[MSGPACK] in accept:
            self.set_header(CONTENT_TYPE, MIME_TYPES[MSGPACK])
            return self.finish(msgpack.dumps(self.normalize(value)))

        if MIME_TYPES[XML] in accept:
            self.set_header(CONTENT_TYPE, MIME_TYPES[XML])
            return self.finish(self.generate_xml(value))

        # JSON
        self.finish(self.normalize(value))

    def write_query_results(self, mapping):
        """Take mapping, query it and turn the resulting query object
        into a dict data structure that will be used by other methods invoked
        by restful_write for representing the output.

        :param apiary.models.base.Base mapping: The mapping to query for

        """
        limit = self.get_argument('limit', None)
        offset = self.get_argument('offset', None)
        filter = self.get_argument('filter', None)
        values = self.query(mapping, limit, offset, filter)
        self.restful_write({"rows": len(values),
                            "limit": limit,
                            "offset": int(offset) if offset else None,
                            "filter": filter,
                            "values": values})

    def write_mapping(self, mapping):
        """Write out a single mapping object

        :param apiary.models.base.Base mapping: The mapping to respond with

        """
        self.restful_write(mapping)
