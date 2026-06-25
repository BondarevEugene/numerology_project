"""
==========================================================
GENESIS HR®

Persistence Engine

Base Storage Interface

Version:
1.0

Description:
Абстрактный интерфейс любого хранилища знаний.

Все реализации (JSON, PostgreSQL, Neo4j и др.)
обязаны реализовать эти методы.
==========================================================
"""

from abc import ABC
from abc import abstractmethod


class Storage(ABC):

    @abstractmethod
    def save(self, entity):
        pass

    @abstractmethod
    def load(self, entity_id):
        pass

    @abstractmethod
    def delete(self, entity_id):
        pass

    @abstractmethod
    def exists(self, entity_id):
        pass

    @abstractmethod
    def list(self, entity_type):
        pass

    @abstractmethod
    def statistics(self):
        pass