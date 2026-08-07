"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®

Skill Model

BUILD 0101

═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Skill:

    id: str

    name: str

    category: str

    description: str = ""

    difficulty: int = 1

    competencies: List[str] = field(default_factory=list)

    professions: List[str] = field(default_factory=list)

    tags: List[str] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)

    enabled: bool = True

    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "difficulty": self.difficulty,
            "competencies": self.competencies,
            "professions": self.professions,
            "tags": self.tags,
            "metadata": self.metadata,
            "enabled": self.enabled,
        }

    @classmethod
    def from_dict(cls, data):

        return cls(**data)