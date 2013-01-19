"""
Login and Logout Request Handlers

"""

from apiary import web
from apiary.authentication import ldapclient
import logging

LOGGER = logging.getLogger()


class Login(web.InterfaceRequestHandler):

    def authentication_error(self, username):
        """Render the login form with the authentication error"""
        self.render('interface/pages/login.html', username=username,
                    login_error=True)

    def connection_error(self):
        """Render the login form with the connection error"""
        LOGGER.critical('Could not connect to LDAP server')
        self.render('interface/pages/login.html', connection_error=True)

    @property
    def ldap_settings(self):
        """Return the LDAP configuration document.

        :rtype: dict

        """
        return self.config.get('ldap')

    def get(self, *args, **kwargs):
        self.render('interface/pages/login.html')

    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        if not username or not password:
            LOGGER.warning('Missing username or password')
            return self.authentication_error(None)
        settings = self.ldap_settings
        try:
            user = ldapclient.LDAPClient(settings['uri'],
                                         username, password,
                                         settings['base_dn']['people'],
                                         settings['base_dn']['groups'])
        except ldapclient.AuthenticationError:
            LOGGER.warning('Authentication error for %s', username)
            return self.authentication_error(username)
        except ldapclient.ConnectionError:
            return self.connection_error()
        self.session.authenticated = True
        self.session.profile = user.user_profile(username)
        self.session.groups = user.groups(username)

        if not self.has_group_access(settings['groups']['access']):
            LOGGER.warning('No group access for %s' % username)
            self._clear_session()
            return self.permission_denied()

        self.redirect('/')


class Logout(web.InterfaceRequestHandler):
    def get(self, *args, **kwargs):
        self._clear_session()
        self.redirect('/')
