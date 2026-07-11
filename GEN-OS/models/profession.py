"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®

Profession Model

BUILD 0102
═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Profession:

    id: str

    name: str

    category: str

    description: str = ""

    competencies: List[str] = field(default_factory=list)

    skills: List[str] = field(default_factory=list)

    vacancies: List[str] = field(default_factory=list)

    courses: List[str] = field(default_factory=list)

    level: str = "Junior"

    salary_min: int = 0

    salary_max: int = 0

    tags: List[str] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)

    enabled: bool = True

    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "competencies": self.competencies,
            "skills": self.skills,
            "vacancies": self.vacancies,
            "courses": self.courses,
            "level": self.level,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "tags": self.tags,
            "metadata": self.metadata,
            "enabled": self.enabled
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)