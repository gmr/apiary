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
        for key in mapping.__table__.columns.keys():
            setattr(mapping, key, self.parameter_value(key, kwargs))

    def generate_xml(self, value_in):

        if isinstance(value_in, dict):
            print value_in
            root = etree.Element(value_in['values'][0].__class__.__name__)

            for key in ['filter', 'limit', 'offset']:
                node = etree.Element(key)
                node.text = str(value_in.get(key))
                root.append(node)

            values = etree.Element('values')
            for row in value_in['values']:
                item = etree.Element(row.__class__.__name__)
                for key in row.__table__.columns.keys():
                    value = getattr(row, key)
                    if isinstance(value, uuid.UUID):
                        value = str(value)
                    node = etree.Element(key)
                    node.text = value
                    item.append(node)
                values.append(item)
            root.append(values)
        else:
            root = etree.Element(value_in.__class__.__name__)
            for key in value_in.__table__.columns.keys():
                value = getattr(value_in, key)
                if isinstance(value, uuid.UUID):
                    value = str(value)
                node = etree.Element(key)
                node.text = value
                root.append(node)
        return etree.tostring(root, pretty_print=True)

    def normalize_mapping_list(self, values_in):
        values_out = list()
        for value in values_in:
            values_out.append(self.normalize_mapping(value))
        return values_out

    def normalize_mapping(self, value_in):
        value_out = dict()
        for key in value_in.__table__.columns.keys():
            value = getattr(value_in, key)
            if isinstance(value, uuid.UUID):
                value = str(value)
            value_out[key] = value
        return value_out

    def parameter_value(self, key, kwargs):
        return kwargs.get(key, self.get_argument(key, None))

    def query(self, mapping, limit, offset, filter):
        query = self.database.query(mapping)
        if offset:
            query = query.offset(offset)

        if limit:
            query = query.limit(limit)


        #if filter:
        #    filter = query.limit(limit)



        return query.all()

    def normalize(self, value):
        if isinstance(value, dict):
            value['values'] = self.normalize_mapping_list(value['values'])
        else:
            value = self.normalize_mapping(value)
        return value

    def restful_write(self, value):

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
        self.restful_write(mapping)
