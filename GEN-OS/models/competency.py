"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
Competency Model

BUILD 0101
Author:
Yevhenii Bondariev
OpenAI GPT-5.5

═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Competency:
    id: str
    name: str
    category: str
    description: str = ""
    level: int = 0
    weight: float = 1.0
    skills: List[str] = field(default_factory=list)
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
            "level": self.level,
            "weight": self.weight,
            "skills": self.skills,
            "professions": self.professions,
            "tags": self.tags,
            "metadata": self.metadata,
            "enabled": self.enabled,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
