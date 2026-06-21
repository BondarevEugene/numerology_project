"""
==========================================================
GENESIS HR®
Base Knowledge Entity
Все сущности Genesis наследуются отсюда.
==========================================================
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class BaseEntity:
    id: str
    title: str
    entity_type: str
    description: str = ""
    tags: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    enabled: bool = True
    version: int = 1
