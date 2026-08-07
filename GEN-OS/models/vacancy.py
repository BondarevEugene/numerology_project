"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®

Vacancy Model

BUILD 0102
═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Vacancy:
    id: str
    title: str
    company: str
    location: str = ""
    remote: bool = False
    salary_min: int = 0
    salary_max: int = 0
    competencies: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    profession: str = ""
    experience: str = "Junior"
    tags: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    enabled: bool = True

    def to_dict(self):

        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "remote": self.remote,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "competencies": self.competencies,
            "skills": self.skills,
            "profession": self.profession,
            "experience": self.experience,
            "tags": self.tags,
            "metadata": self.metadata,
            "enabled": self.enabled
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)