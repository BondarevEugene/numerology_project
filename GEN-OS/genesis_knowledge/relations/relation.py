"""
==========================================================
GENESIS HR®
Knowledge Graph
Relation
Version:1.0
==========================================================
"""

from dataclasses import dataclass
from datetime import datetime

from .relation_types import RelationType


@dataclass
class Relation:
    source: str
    target: str
    relation: RelationType
    weight: int = 100
    description: str = ""
    created_at: datetime = datetime.utcnow()

    def to_dict(self):
        return {
            "source": self.source,
            "target": self.target,
            "relation": self.relation.value,
            "weight": self.weight,
            "description": self.description
        }
