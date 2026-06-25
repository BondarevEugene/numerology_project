"""
════════════════════════════════════════════════════════════════════

GENESIS HR®
Knowledge Core

Module: Entity Registry

File: entity_factory.py

Purpose: Creates Entity objects from any data source.

Supported:
• Excel
• CSV
• JSON
• API
• ESCO
• O*NET
• AI
════════════════════════════════════════════════════════════════════
"""

from collections import defaultdict
from typing import Any
from typing import Dict
from typing import Optional

from .entity import Entity
from .enums import EntitySource
from .enums import EntityStatus
from .enums import EntityType


class EntityFactory:

    def __init__(self):
        self._counters = defaultdict(int)
        self._prefix = {
            EntityType.PROFESSION: "GEN-PROF",
            EntityType.COMPETENCY: "GEN-COMP",
            EntityType.ARCHETYPE: "GEN-ARCH",
            EntityType.SKILL: "GEN-SKIL",
            EntityType.HABIT: "GEN-HABT",
            EntityType.SPORT: "GEN-SPRT",
            EntityType.BOOK: "GEN-BOOK",
            EntityType.COURSE: "GEN-CRSE",
            EntityType.UNIVERSITY: "GEN-UNIV",
            EntityType.CERTIFICATION: "GEN-CERT",
            EntityType.PROJECT: "GEN-PROJ",
            EntityType.INDUSTRY: "GEN-INDU",
            EntityType.TECHNOLOGY: "GEN-TECH",
            EntityType.TOOL: "GEN-TOOL",
            EntityType.LANGUAGE: "GEN-LANG",
            EntityType.COMPANY: "GEN-COMPANY",
            EntityType.ROLE: "GEN-ROLE",
            EntityType.TASK: "GEN-TASK",
            EntityType.PROTOCOL: "GEN-PROT",
            EntityType.ENVIRONMENT: "GEN-ENVR",
            EntityType.PERSONALITY_TRAIT: "GEN-TRAI",
            EntityType.VALUE: "GEN-VALU",
            EntityType.INTEREST: "GEN-INTR",
            EntityType.HOBBY: "GEN-HOBB",
            EntityType.MARKET: "GEN-MARK",
            EntityType.COUNTRY: "GEN-CNTR",
            EntityType.CITY: "GEN-CITY",
            EntityType.SALARY: "GEN-SALR",
            EntityType.EDUCATION: "GEN-EDUC",
            EntityType.OTHER: "GEN-OTHR"
        }

    def next_id(
        self,
        entity_type: EntityType
    ) -> str:
        self._counters[entity_type] += 1
        prefix = self._prefix.get(
            entity_type,
            "GEN-OTHR"
        )

        return f"{prefix}-{self._counters[entity_type]:06d}"

    def create(
        self,
        entity_type: EntityType,
        title: str,
        description: str = "",
        code: Optional[str] = None,
        source: EntitySource = EntitySource.MANUAL,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Entity:

        return Entity(
            id=self.next_id(entity_type),
            type=entity_type,
            title=title.strip(),
            code=code,
            description=description,
            source=source,
            status=EntityStatus.DRAFT,
            metadata=metadata or {}
        )

    def create_from_dict(
        self,
        entity_type: EntityType,
        data: Dict[str, Any],
        source: EntitySource
    ) -> Entity:
        entity = self.create(
            entity_type=entity_type,
            title=data.get("title", ""),
            description=data.get("description", ""),
            code=data.get("code"),
            source=source,
            metadata=data
        )

        aliases = data.get("aliases", [])
        if isinstance(aliases, list):
            for alias in aliases:
                entity.add_alias(alias)
        tags = data.get("tags", [])
        if isinstance(tags, list):
            for tag in tags:
                entity.add_tag(tag)
        return entity
