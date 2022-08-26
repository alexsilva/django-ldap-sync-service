import json

from ldap3 import Server, Connection, ALL, NTLM, SUBTREE

from ldap_sync import service


class LdapSearchBindException(service.LdapSearchException):
    """ Exception raised when bind does not occur as expected """


class LdapSearchService(service.LdapSearch):
    """Implements the service interface"""

    def __init__(self, uri, **options):
        super(LdapSearchService, self).__init__(uri)
        options.setdefault('get_info', ALL)
        self.server = Server(uri, **options)
        self._conn = self.username = self.password = None

    def get_connection(self, **options):
        """Initiates a new connection to the server"""
        options.setdefault('authentication', NTLM)
        options.setdefault('user', self.username)
        options.setdefault('password', self.password)
        return Connection(self.server, **options)

    @property
    def connection(self):
        if self._conn is None:
            self._conn = self.get_connection()
        return self._conn

    @connection.setter
    def connection(self, conn):
        """Change current connection"""
        self._conn = conn

    def users(self, sbase, sfilter, attributes):
        """Search for users"""
        entry_generator = self.connection.extend.standard.paged_search(
            search_base=sbase,
            search_filter=sfilter,
            attributes=attributes,
            search_scope=SUBTREE,
            paged_size=5,
            generator=True)
        storage = []
        total_entries = 0
        for entry in entry_generator:
            total_entries += 1
            attributes = entry.setdefault('attributes', {})
            attrs = dict(attributes)  # copy
            storage.append(attrs)
            if total_entries % 100 == 0:
                yield storage
                storage = []
        yield storage

    def groups(self, sbase, sfilter, attributes):
        """Search for groups"""
        return []

    def login(self, username, password):
        """make login"""
        self.username = username
        self.password = password

        conn = self.connection
        result = conn.bind()
        if not result:
            raise LdapSearchBindException('error in bind {0.result}'.format(conn))
        return result
