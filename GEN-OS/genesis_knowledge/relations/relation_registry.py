"""
Registry всех связей системы.
"""

from .relation import Relation


class RelationRegistry:

    def __init__(self):

        self._relations=[]

    def add(self,relation):

        self._relations.append(relation)

    def all(self):

        return self._relations

    def count(self):

        return len(self._relations)

    def clear(self):

        self._relations.clear()