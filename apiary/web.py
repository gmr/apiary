"""
Base RequestHandlers for both the API and web interface

"""
import datetime
from lxml import etree
import json
import logging
import msgpack
import uuid
from tornado import web

from apiary.mappers import session

LOGGER = logging.getLogger(__name__)

# Pass-through Tornado method decorators
asynchronous = web.asynchronous
authenticated = web.authenticated


class BaseRequestHandler(web.RequestHandler):
    """Common base request handler for both API and Interface"""

    @property
    def accept_header(self):
        """Return a list of mime types from the accept header as a list of
        strings.

        :rtype: list

        """
        return self.request.headers.get('Accept').split(';')[0].split(',')

    def initialize(self):
        """Initialize the request handler, setting shortcuts to the database
        and configuration values from the tornado.Application instance.

        """
        self.database = self.application.database
        self.config = self.application.apiary_config

    def new_query(self, mapping):
        """Create a SQLAlchemy Query object for the given mapping

        :param apiary.mappers.base.Base mapping: The mapping to query
        :rtype: sqlalchemy.query.Query

        """
        return self.database.query(mapping)

    def query(self, mapping, limit=None, offset=None, filter=None):
        """Create and execute a query for the mapping type, applying the limit,
        offset and filter if specified.


        :param apiary.mappers.base.Base mapping: The mapping class to query for
        :param int limit: Number of rows to limit to (optional)
        :param int offset: The row offset (optional)
        :param str filter: The filter to reply
        :rtype: list

        """
        query = self.database.query(mapping)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        #if filter:
        #    query = query.filter(filter)
        return query.all()


class APIRequestHandler(BaseRequestHandler):
    """Generic base RequestHandler for the RESTful API set that minimizes the
    duplicate functionality across all the APIs. This RequestHandler will send
    different types of output for the request based upon the Accept header and
    will take SQLAlchemy mappers/mappings and extract the data out.

    """
    CONTENT_TYPE = 'Content-Type'
    HTML = 'html'
    JSONP = 'jsonp'
    MSGPACK = 'msgpack'
    XML = 'xml'

    MIME_TYPES = {JSONP: 'application/javascript',
                  HTML: 'text/html',
                  MSGPACK: 'application/x-msgpack',
                  XML: 'text/xml'}

    JSONP_METHOD = 'on_jsonp'

    def assign_attributes(self, mapping, kwargs):
        """Assign values passed in via either a GET/POST values or via URI
        parsing to a mapping object.

        :param apiary.mappers.base.Base mapping: The mapping object
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

        :param apiary.mappers.base.Base value_in: The mapping value
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

        :param apiary.mappers.base.Base|dict: The item or a multi-item dict
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

        :param apiary.mappers.base.Base value_in: The mapping object
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

    def normalize(self, value):
        """Take the inbound value and normalize the values returning a python
        dict instead of whatever mapping related type was passed in.

        :param apiary.mappers.base.Base|dict value: The value to normalize
        :rtype: dict

        """
        if isinstance(value, dict):
            value['values'] = self.normalize_mapping_list(value['values'])
        else:
            value = self.normalize_mapping(value)
        return value

    def restful_write(self, value):
        """Handle the outbound writing for the request, applying logic against
        the Accept header to decide how the value should be returned.

        :param apiary.mappers.base.Base|list value: The value to send

        """
        accept = self.accept_header
        LOGGER.debug('Accept headers: %r', accept)

        # HTML
        if  self.MIME_TYPES[self.HTML] in accept:
            self.set_header(self.CONTENT_TYPE, self.MIME_TYPES[self.HTML])
            if isinstance(value, dict):
                return self.render('api/table.html', values=value)
            return self.render('api/item.html', value=value)

        # JSON-P
        if self.MIME_TYPES[self.JSONP] in accept:
            method_name = self.get_argument('callback', self.JSONP_METHOD)
            self.set_header(self.CONTENT_TYPE, self.MIME_TYPES[self.JSONP])
            return self.finish('%s(%s)' % (method_name,
                                           json.dumps(self.normalize(value),
                                                      ensure_ascii=False)))

        # MsgPack
        if self.MIME_TYPES[self.MSGPACK] in accept:
            self.set_header(self.CONTENT_TYPE, self.MIME_TYPES[self.MSGPACK])
            return self.finish(msgpack.dumps(self.normalize(value)))

        if self.MIME_TYPES[self.XML] in accept:
            self.set_header(self.CONTENT_TYPE, self.MIME_TYPES[self.XML])
            return self.finish(self.generate_xml(value))

        # JSON
        self.finish(self.normalize(value))

    def write_query_results(self, mapping):
        """Take mapping, query it and turn the resulting query object
        into a dict data structure that will be used by other methods invoked
        by restful_write for representing the output.

        :param apiary.mappers.base.Base mapping: The mapping to query for

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

        :param apiary.mappers.base.Base mapping: The mapping to respond with

        """
        self.restful_write(mapping)


class InterfaceRequestHandler(BaseRequestHandler):
    """Base Request Handler for the web interface"""
    DEFAULT_LOCALE = 'en-US'
    DURATION = 'duration'
    NAME = 'cookie_name'

    COOKIE_NAME = 'session'
    COOKIE_DURATION = 3600

    def get_current_user(self):
        """Called by Tornado to get the current user, if there is an
        authenticated session. If there is no user, return None.

        :rtype: dict

        """
        if self.session.authenticated:
            LOGGER.debug('User is authenticated')
        return self.session.profile or None

    def has_group_access(self, groups):
        """Check to see if the current user has an intersection in any of the
        groups required and their group memberships.

        :param list groups: The list of groups to check
        :rtype: bool

        """
        if not groups:
            LOGGER.warning('No groups passed in to validate: %r', groups)
            return False
        return any([group for group in self.session.groups or list()
                    if group in groups])

    def in_group(self, group):
        """Returns bool if the user is a member of the configured group of
        groups as specified in the ldap configuration for the application.

        :param str group: The group name for the list of groups
        :rtype: bool

        """
        groups = self.config['ldap'].get('groups')
        return self.has_group_access(groups.get(group))

    def on_finish(self):
        """Called by Tornado when the request is done. Save the request and
        remove the redis connection.

        """
        super(InterfaceRequestHandler, self).on_finish()

        # Update the session in the database with the values from this request
        self._update_session_values()

        # Make sure the session is not persisted in this object across requests
        if hasattr(self, 'session'):
            del self.session

    def permission_denied(self):
        """Return a 403 page when trying to access a page that a user does not
        have access to.

        """
        self.render("interface/errors/403.html",
                    page_name="Error: Permission Denied")
        self.set_status(403)

    def prepare(self):
        """Prepare the session, setting up the session object and loading in
        the values, assigning the IP address to the session if it's an new one.

        """
        super(InterfaceRequestHandler, self).prepare()
        self.session = self._get_session_object()
        if not self.session:
            LOGGER.warning('Could not create session object')

        # Always send a new session cookie to update the expiration
        self._set_session_cookie()

        LOGGER.debug('Session ID: %s', self.session.id)

    def render(self, template_name, **kwargs):
        """Override the render method to inject the user preferences and the
        class name in as the "page" global variable.

        """
        LOGGER.debug('In parent render')
        kwargs['page'] = self.__class__.__name__
        kwargs['preferences'] = self._get_user_preferences()
        kwargs['in_group'] = self.in_group
        super(InterfaceRequestHandler, self).render(template_name, **kwargs)

    def _clear_session(self):
        """Clear the user's sessions, resetting the cookies and removing the
        data from redis.

        """
        LOGGER.info('Clearing session')
        self.database.delete(self.session)
        self.database.commit()
        self.clear_cookie(self._session_cookie_name)

    def _create_session(self):
        """Create a new session, returning the mapping object for the session
        data.

        :rtype: apiary.mappings.session.Session

        """
        LOGGER.debug('Creating a new session')
        session_obj = session.Session()
        session_obj.remote_ip = self.request.remote_ip
        session_obj.last_request_uri = self.request.uri
        self.database.add(session_obj)
        self.database.commit()
        return session_obj

    def _get_session_object(self):
        """Return an instance of the session object for the current session.
        If there is no pre-existing session, the session object will be created
        with a new session id.

        :rtype: tinman.session.SessionAdapter

        """
        LOGGER.debug('Querying for the session')
        if not self._session_id:
            return self._create_session()
        return self.database.query(session.Session).get(self._session_id)

    def _get_user_preferences(self):
        """Return the user preferences as a dict.

        :rtype: dict

        """
        return {}

    @property
    def _session_expiration(self):
        """Return the expiration timestamp for the session cookie.

        :rtype: datetime

        """
        value = (datetime.datetime.utcnow() +
                 datetime.timedelta(seconds=self._session_duration))
        LOGGER.debug('Cookie expires: %s', value.isoformat())
        return value

    @property
    def _session_cookie_name(self):
        """Return the session cookie name, defaulting to the class default

        :rtype: str

        """
        return self.config.get('session', {}).get(self.NAME, self.COOKIE_NAME)

    @property
    def _session_duration(self):
        """Return the session duration in seconds from the configuration,
        defaulting to the class default.

        :rtype: int

        """
        return self.config.get('session', {}).get(self.DURATION,
                                                  self.COOKIE_DURATION)

    @property
    def _session_id(self):
        """Gets the session id from the session cookie.

        :rtype: str

        """
        return self.get_secure_cookie(self._session_cookie_name, None)

    def _set_session_cookie(self):
        """Set the session data cookie."""
        LOGGER.debug('Setting session cookie for %s', self.session.id)
        self.set_secure_cookie(name=self._session_cookie_name,
                               value=str(self.session.id),
                               expires=self._session_expiration)

    def _update_session_values(self):
        """Update the session object and database with new values, warning if
        the IP address has changed.

        """
        if not hasattr(self, 'session'):
            LOGGER.warning('Session never created')
            return
        if self.session.remote_ip != self.request.remote_ip:
            LOGGER.warning("Session %s IP address has changed from %s to %s",
                           self.session.id, self.session.ip_address,
                           self.request.remote_ip)
            self.session.ip_address = self.request.remote_ip

        if self.session.last_request_uri != self.request.uri:
            self.session.last_request_uri = self.request.uri

        self.session.last_request_at = datetime.datetime.now()
        self.database.merge(self.session)
