"""
==========================================================
GENESIS HR®
Neo4j Storage
Version:
1.0
==========================================================
"""

from .storage import Storage


class Neo4jStorage(Storage):

    def save(self, entity):
        raise NotImplementedError

    def load(self, entity_id):
        raise NotImplementedError

    def delete(self, entity_id):
        raise NotImplementedError

    def exists(self, entity_id):
        raise NotImplementedError

    def list(self, entity_type):
        raise NotImplementedError

    def statistics(self):
        raise NotImplementedError