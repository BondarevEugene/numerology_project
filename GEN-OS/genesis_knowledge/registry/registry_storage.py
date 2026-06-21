"""
==========================================================
GENESIS HR®
Registry Storage

Version:
1.0

Description:
Фасад системы хранения.
==========================================================
"""

from .json_storage import JsonStorage


class RegistryStorage:
    def __init__(self, root="registry"):
        self.backend = JsonStorage(root)

    def save(self, entity):
        return self.backend.save(entity)

    def load(self, entity_id):
        return self.backend.load(entity_id)

    def delete(self, entity_id):
        return self.backend.delete(entity_id)

    def exists(self, entity_id):
        return self.backend.exists(entity_id)

    def list(self, entity_type):
        return self.backend.list(entity_type)

    def statistics(self):
        return self.backend.statistics()
