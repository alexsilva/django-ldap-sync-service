from ldap3 import Server, Connection, ALL, NTLM

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
        items = []
        if self.connection.search(search_base=sbase,
                                  search_filter=sfilter,
                                  attributes=attributes):
            for entry in self.connection.entries:
                attrs = {}
                for attr in attributes:
                    attrs[attr] = getattr(entry, attr)
                data = {
                    "attributes": attrs,
                    "json": entry.entry_to_json()
                }
                items.append(data)
        else:
            raise service.LdapSearchException("empty search")
        return items

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
