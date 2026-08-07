"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®

Course Model

BUILD 0102
═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Course:
    id: str
    title: str
    provider: str
    url: str = ""
    duration: int = 0
    difficulty: str = "Beginner"
    competencies: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    professions: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    enabled: bool = True

    def to_dict(self):

        return {
            "id": self.id,
            "title": self.title,
            "provider": self.provider,
            "url": self.url,
            "duration": self.duration,
            "difficulty": self.difficulty,
            "competencies": self.competencies,
            "skills": self.skills,
            "professions": self.professions,
            "tags": self.tags,
            "metadata": self.metadata,
            "enabled": self.enabled
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)