"""
Functionality for authenticating a user and getting their groups

"""
import ldap
import logging

LOGGER = logging.getLogger(__name__)


class LDAPUser(object):
    """A read-only LDAP user class that connects to the LDAP server and attempts
    to authenticate the user. Provides property methods to make sure the _groups
    and _profile attributes are read only.

    """
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
        self._cn = ldap_user
        self._people_dn = people
        self._groups_dn = groups

        # Connect and anonymously bind to the LDAP server
        self._ldap = self._new_connection(ldap_uri)
        self._bind()

        # Try and find the bind DN for the specified username/cn
        self._bind_dn = self._search_for_dn()
        if not self._bind_dn:
            raise AuthenticationError

        # Try and authenticate the bind dn with the password specified
        try:
            self._simple_bind(self._bind_dn, ldap_password)
        except ldap.INVALID_CREDENTIALS:
            raise AuthenticationError

        # Preload the groups and profile
        self._groups = self._fetch_groups()
        self._profile = self._fetch_profile()

    @property
    def groups(self):
        """Return a new instance of the group list

        :rtype: list

        """
        return list(self._groups) if self._groups else None

    @property
    def profile(self):
        """Return a new instance of the profile values dict

        :rtype: dict

        """
        return dict(self._profile) if self._profile else None

    def _bind(self):
        """Bind to the LDAP server anonymously to get the bind DN for the user.

        """
        LOGGER.debug('Preforming anonymous bind')
        self._simple_bind('', '')

    def _fetch_groups(self):
        """Return the DN of each group that username is a member of.

        :rtype: list

        """
        response = self._ldap.search_s(self._groups_dn,
                                       ldap.SCOPE_SUBTREE,
                                       '(member=%s)' % self._bind_dn,
                                       ['cn'])
        groups = list()
        for group in response:
            groups.append(group[0])
        return groups

    def _fetch_profile(self):
        """Return the profile data for the specified username.

        :rtype: dict

        """
        response = self._ldap.search_s(self._people_dn,
                                       ldap.SCOPE_SUBTREE,
                                       self._cn_search_filter,
                                       self.PROFILE_ATTRIBUTES)
        profile = dict()
        for row in response:
            for key in row[1]:
                if len(row[1][key]) > 1:
                    profile[key] = row[1][key]
                else:
                    profile[key] = row[1][key][0]
        return profile

    def _new_connection(self, uri):
        """Return an active LDAP connection

        :param str uri: The LDAP url for the connection
        :rtype: ldap.connection

        """
        LOGGER.debug('Connecting to %s', uri)
        return ldap.initialize(uri)

    @property
    def _cn_search_filter(self):
        """Returns a cn filter string for ldap.search_s.

        :rtype: str

        """
        return '(cn=%s)' % self._cn

    def _search_for_dn(self):
        """Return the DN for the specified username.

        :rtype: str

        """
        response = self._ldap.search_s(self._people_dn,
                                       ldap.SCOPE_SUBTREE,
                                       self._cn_search_filter, ['cn'])
        if response:
            return response[0][0]
        return None

    def _simple_bind(self, dn, password):
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


class AuthenticationError(Exception):
    pass


class ConnectionError(Exception):
    pass
