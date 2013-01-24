"""
Base RequestHandlers for both the API and web interface

"""
import datetime
from lxml import etree
import base64
import json
import logging
import msgpack
import uuid
import traceback
from tornado import web

from logging import config

from apiary import authentication
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


class AuthRequestHandler(BaseRequestHandler):
    """Base Request Handler for the web interface"""
    DEFAULT_LOCALE = 'en-US'
    DURATION = 'duration'
    NAME = 'cookie_name'

    COOKIE_NAME = 'session'
    COOKIE_DURATION = 3600
    CREATE_SESSION = True

    def error_page(self, message, status_code=500):
        self.set_status(status_code)
        self.render('interface/pages/error.html',
                    status_code=status_code,
                    error_message=message,
                    traceback=traceback.format_stack())

    def get_current_user(self):
        """Called by Tornado to get the current user, if there is an
        authenticated session. If there is no user, return None.

        :rtype: dict

        """
        if self.session:
            return self.session.profile or None
        return None

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
        super(AuthRequestHandler, self).on_finish()

        # Update the session in the database with the values from this request
        self._update_session_values()

        # Make sure the session is not persisted in this object across requests
        if hasattr(self, 'session'):
            del self.session

    def permission_denied(self):
        """Return a 403 page when trying to access a page that a user does not
        have access to.

        """
        self.error_page("Permission Denied", 403)

    def prepare(self):
        """Prepare the session, setting up the session object and loading in
        the values, assigning the IP address to the session if it's an new one.

        """
        super(AuthRequestHandler, self).prepare()
        self.session = self._get_session_object()
        if not self.session and self.CREATE_SESSION:
            LOGGER.warning('Could not create session object')
            self.clear_cookie(self._session_cookie_name)
            return self.error_page('Could not create session')

        # Always send a new session cookie to update the expiration
        if self.CREATE_SESSION:
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
        super(AuthRequestHandler, self).render(template_name, **kwargs)

    def _authenticate(self, username, password):
        """Attempt to authenticate the user with the given username and password

        :rtype: apiary.ldapclient.LDAPUser
        :raises: apiary.ldapclient.AuthenticationError
        :raises: apiary.ldapclient.ConnectionError

        """
        settings = self._ldap_settings
        try:
            user = authentication.LDAPUser(settings['uri'],
                                           username, password,
                                           settings['base_dn']['people'],
                                           settings['base_dn']['groups'])
        except authentication.AuthenticationError as error:
            LOGGER.warning('Authentication error for %s', username)
            raise error
        except authentication.ConnectionError as error:
            LOGGER.warning('Could not connect to LDAP server: %s', error)
            raise error
        return user

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
        with a new session id. If the class attribute CREATE_SESSION is False,
        None will be returned. This is used in the API request handler that
        allows for both session auth and HTTP Basic Auth

        :rtype: tinman.session.SessionAdapter or None

        """
        LOGGER.debug('Querying for the session')
        if not self._session_id:
            if self.CREATE_SESSION:
                return self._create_session()
            else:
                return None
        return self.database.query(session.Session).get(self._session_id)

    def _get_user_preferences(self):
        """Return the user preferences as a dict.

        :rtype: dict

        """
        return {}
    @property
    def _ldap_settings(self):
        """Return the LDAP configuration document.

        :rtype: dict

        """
        return self.config.get('ldap')

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
        if not hasattr(self, 'session') or not self.session:
            return
        if self.session.remote_ip != self.request.remote_ip:
            LOGGER.warning("Session %s IP address has changed from %s to %s",
                           self.session.id, self.session.remote_ip,
                           self.request.remote_ip)
            self.session.remote_ip = self.request.remote_ip

        if self.session.last_request_uri != self.request.uri:
            self.session.last_request_uri = self.request.uri

        self.session.last_request_at = datetime.datetime.now()
        self.database.merge(self.session)


class APIRequestHandler(AuthRequestHandler):
    """Generic base RequestHandler for the RESTful API set that minimizes the
    duplicate functionality across all the APIs. This RequestHandler will send
    different types of output for the request based upon the Accept header and
    will take SQLAlchemy mappers/mappings and extract the data out.

    Authorization is required for all API access and will try and use a session
    if a session exists so that the web UI can use the API natively. If there
    is no session, instead of creating one, it will instead use HTTP basic auth
    to validate the user.

    """
    AUTH_REALM = 'Apiary API Access'
    CREATE_SESSION = False

    CONTENT_TYPE = 'Content-Type'
    HTML = 'html'
    JSON = 'json'
    JSONP = 'jsonp'
    MSGPACK = 'msgpack'
    XML = 'xml'

    MIME_TYPES = {JSON: 'application/json',
                  JSONP: 'application/javascript',
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

    def get_basic_auth_user(self):
        """Attempt to get the user via HTTP basic-auth

        :rtype: dict

        """
        authorization = self.request.headers.get('Authorization')
        if not authorization or authorization[0:6] != 'Basic ':
            return None

        username, password = self.parse_authorization_header(authorization)
        self._authenticated_user = self._authenticate(username, password)
        if not self._authenticated_user:
            return None
        return self._authenticated_user.profile

    def get_current_user(self):
        """Called by Tornado to get the current user, if there is an
        authenticated session. If there is no user, return None.

        :rtype: dict

        """
        if self.session:
            LOGGER.debug('There is a session object')
            if self.session.authenticated:
                LOGGER.debug('User is authenticated')
                return self.session.profile or None
        return self.get_basic_auth_user()

    def has_group_access(self, groups):
        """Check to see if the current user has an intersection in any of the
        groups required and their group memberships.

        :param list groups: The list of groups to check
        :rtype: bool

        """
        if not groups:
            LOGGER.warning('No groups passed in to validate: %r', groups)
            return False
        group_list = list()
        if self.session:
            group_list += self.session.groups
        if self._authenticated_user.groups:
            group_list += self._authenticated_user.groups
        return any([group for group in group_list if group in groups])

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
        if isinstance(value_in, list):
            return self.normalize_mapping_list(value_in)

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

    def parse_authorization_header(self, value):
        """Take the inbound authorization header and return a tuple of username
        and password.

        Inbound value looks like:  Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==

        :rtype: username, password

        """
        decoded = base64.b64decode(value.split(' ')[-1])
        return decoded.split(':')

    def prepare(self):
        """Ensure that all API requests are authenticated. If there is no
        current user, unauthorized_request will send the proper headers and
        raise an HTTPError exception to keep Tornado from dispatching the
        request any further.

        """
        super(APIRequestHandler, self).prepare()
        self._authenticated_user = None
        if not self.current_user:
            self.unauthorized_request()

    def restful_write(self, value):
        """Handle the outbound writing for the request, applying logic against
        the Accept header to decide how the value should be returned.

        :param apiary.mappers.base.Base|list value: The value to send

        """
        accept = self.accept_header

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
        self.set_header(self.CONTENT_TYPE, self.MIME_TYPES[self.JSON])
        self.finish(json.dumps(self.normalize(value), ensure_ascii=False))

    def unauthorized_request(self):
        """Set the appropriate headers and close out the request which will keep
        get/post/delete etc from processing.

        """
        self.set_status(401)
        self.set_header('WWW-Authenticate',
                        'Basic realm="%s"' % self.config.get('auth_realm',
                                                             self.AUTH_REALM))
        self.finish()

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
        self.restful_write(values)

    def write_mapping(self, mapping):
        """Write out a single mapping object

        :param apiary.mappers.base.Base mapping: The mapping to respond with

        """
        self.restful_write(mapping)
