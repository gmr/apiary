"""
Base API Class

"""
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

        # JSON
        self.write(self.normalize(value))

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
