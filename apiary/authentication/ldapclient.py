"""
Functionality for authenticating a user and getting their groups

"""
import ldap
import logging

LOGGER = logging.getLogger(__name__)


class LDAPClient(object):

    PROFILE_ATTRIBUTES = ['cn', 'displayName', 'email', 'gidNumber',
                          'givenName', 'l', 'loginShell', 'mail',
                          'mailLocalAccess','sn', 'uid', 'uidNumber']

    def __init__(self, ldap_uri, ldap_user, ldap_password, people, groups):
        """Create a Password object

        :param str ldap_uri: The LDAP url for the connection
        :param str ldap_user: The user to bind as
        :param str ldap_password: The password to use
        :param str people: The base DN to search for users with
        :param str groups: The base DN to search for groups with
        :rtype: ldap.connection

        """
        self._people = people
        self._groups = groups
        self._ldap = self._get_ldap_connection(ldap_uri)
        self._anonymous_bind()
        bind_dn = self._get_dn_from_username(ldap_user)
        if not bind_dn:
            raise AuthenticationError
        try:
            self._bind_user(bind_dn, ldap_password)
        except ldap.INVALID_CREDENTIALS:
            raise AuthenticationError

    def _get_ldap_connection(self, uri):
        """Return an active LDAP connection

        :param str uri: The LDAP url for the connection
        :rtype: ldap.connection

        """
        LOGGER.debug('Connecting to %s', uri)
        return ldap.initialize(uri)

    def _anonymous_bind(self):
        """Bind to the LDAP server anonymously to get the bind DN for the user.

        """
        LOGGER.debug('Preforming anonymous bind')
        self._bind_user('', '')

    def _bind_user(self, dn, password):
        """Bind the specified DN using the password.

        :param str dn: The DN to bind to
        :param str password: The password to use

        """
        LOGGER.debug('Performing LDAP bind to DN: %s', dn or 'anonymous')
        try:
            return self._ldap.simple_bind_s(dn, password)
        except TypeError as error:
            LOGGER.error('Error binding %s: %s', error)
            raise ldap.INVALID_CREDENTIALS
        except ldap.SERVER_DOWN:
            raise ConnectionError

    def _get_dn_from_username(self, username):
        """Return the DN for the specified username.

        :param str username: The user to bind as
        :rtype: str

        """
        LOGGER.debug('Searching for %s', username)
        response = self._ldap.search_s(self._people,
                                       ldap.SCOPE_SUBTREE,
                                       '(cn=%s)' % username, ['cn'])
        if response:
            return response[0][0]
        return None

    def user_profile(self, username):
        """Return the profile data for the specified username.

        :param str username: The username for the profile data.
        :rtype: dict

        """
        response = self._ldap.search_s(self._people,
                                       ldap.SCOPE_SUBTREE,
                                       '(cn=%s)' % username,
                                       self.PROFILE_ATTRIBUTES)
        profile = dict()
        for row in response:
            for key in row[1]:
                if len(row[1][key]) > 1:
                    profile[key] = row[1][key]
                else:
                    profile[key] = row[1][key][0]
        return profile

    def groups(self, username):
        """Return the DN of each group that username is a member of.

        :param str username: The username to get the groups for
        :rtype: list

        """
        dn = self._get_dn_from_username(username)
        response = self._ldap.search_s(self._groups,
                                       ldap.SCOPE_SUBTREE,
                                       '(member=%s)' % dn,
                                       ['cn'])
        LOGGER.debug('Response: %r', response)
        groups = list()
        for group in response:
            groups.append(group[0])
        return groups


class AuthenticationError(Exception):
    pass


class ConnectionError(Exception):
    pass
