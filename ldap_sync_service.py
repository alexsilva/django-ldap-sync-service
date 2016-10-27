from ldap_sync.service import Service
from pyad import *


class PyadService(Service):
    """Implements the service interface"""

    def __init__(self, uri):
        super(PyadService, self).__init__(uri)
        pyad.set_defaults(ldap_server=uri)

    def _search_users(self, base, filter, attributes):
        """Search for users"""
        groups = adgroup.ADGroup.from_dn(filter + "," + base)
        users = []
        for user in groups.get_members():
            users.append((user.cn, {k: (getattr(user, k),) for k in attributes}))
        return users

    def _search_groups(self, base, filter, attributes):
        return []

    def search(self, base, filter, attributes, objectype=None):
        """generic search"""
        return getattr(self, '_search_' + objectype)(base, filter, attributes)

    def login(self, username, password):
        """make login"""
        pyad.set_defaults(username=username, password=password)
