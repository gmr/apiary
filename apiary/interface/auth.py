"""
Login and Logout Request Handlers

"""
import logging

from apiary import authentication
from apiary import web

LOGGER = logging.getLogger()


class Login(web.AuthRequestHandler):
    """Login request handler processes requests for the login form (GET) and
    authentication requests (POST).

    """
    def authentication_error(self, username):
        """Render the login form with the authentication error"""
        self.render('interface/pages/login.html', username=username,
                    login_error=True)

    def connection_error(self):
        """Render the login form with the connection error"""
        LOGGER.critical('Could not connect to LDAP server')
        self.render('interface/pages/login.html', connection_error=True)

    def get(self, *args, **kwargs):
        if self.session and self.session.authenticated:
            return self.redirect('/')
        self.render('interface/pages/login.html')

    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        if not username or not password:
            LOGGER.warning('Missing username or password')
            return self.authentication_error(None)
        try:
            user = self._authenticate(username, password)
        except authentication.AuthenticationError:
            LOGGER.warning('Authentication error for %s', username)
            return self.authentication_error(username)
        except authentication.ConnectionError:
            return self.connection_error()
        self.session.authenticated = True
        self.session.profile = user.profile
        self.session.groups = user.groups
        if not self.has_group_access(self._ldap_settings['groups']['access']):
            LOGGER.warning('No group access for %s' % username)
            self._clear_session()
            return self.permission_denied()
        self.redirect('/')


class Logout(web.AuthRequestHandler):
    """Log the user out of the session, clearing the session and redirecting
    them to the login page.

    """
    def get(self, *args, **kwargs):
        self._clear_session()
        self.render('interface/pages/login.html', logged_out=True)
