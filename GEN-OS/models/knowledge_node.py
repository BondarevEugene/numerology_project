"""
═══════════════════════════════════════════════════════════════════════
GENESIS®
Knowledge Graph Node
BUILD 0103

═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass, field
from uuid import uuid4
from typing import Dict, List


@dataclass
class KnowledgeNode:
    id: str = field(default_factory=lambda: str(uuid4()))
    type: str = "node"
    name: str = ""
    description: str = ""
    tags: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    enabled: bool = True

    def to_dict(self):

        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "metadata": self.metadata,
            "enabled": self.enabled
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
