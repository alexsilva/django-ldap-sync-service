import json

from ldap3 import Server, Connection, ALL, NTLM, SUBTREE

from ldap_sync import service


class LdapSearchBindException(service.LdapSearchException):
    """ Exception raised when bind does not occur as expected """


class LdapSearchService(service.LdapSearch):
    """Implements the service interface"""

    def __init__(self, uri):
        super(LdapSearchService, self).__init__(uri)

        self.server = Server(uri, get_info=ALL)
        self._conn = self.username = self.password = None

    @property
    def connection(self):
        if self._conn is None:
            self._conn = Connection(self.server,
                                    user=self.username,
                                    password=self.password,
                                    authentication=NTLM)
        return self._conn

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
            attributes = entry['attributes']
            attrs = dict(attributes)
            data = {
                "attributes": attrs,
                "json": json.dumps(attrs)
            }
            storage.append(data)
            if total_entries % 100 == 0:
                yield storage
                storage = []
        yield storage
        raise StopIteration

    def groups(self, sbase, sfilter, attributes):
        """Search for groups"""
        return []

    def login(self, username, password):
        """make login"""
        self.username = username
        self.password = password

        conn = self.connection

        if not conn.bind():
            raise LdapSearchBindException('error in bind {0.result}'.format(conn))
