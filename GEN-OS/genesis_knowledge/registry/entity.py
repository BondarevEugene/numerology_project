"""
════════════════════════════════════════════════════════════════════
GENESIS HR®
Knowledge Core

Module:Entity Registry
File:entity.py
Purpose:Universal knowledge object.
Every object inside Genesis is represented as an Entity.
════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from .enums import ConfidenceLevel
from .enums import EntitySource
from .enums import EntityStatus
from .enums import EntityType


@dataclass
class Entity:
    id: str
    type: EntityType
    title: str
    code: Optional[str] = None
    description: str = ""
    aliases: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    source: EntitySource = EntitySource.MANUAL
    status: EntityStatus = EntityStatus.DRAFT
    confidence: ConfidenceLevel = ConfidenceLevel.UNKNOWN
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    version: int = 1

    def touch(self) -> None:
        self.updated_at = datetime.utcnow()
        self.version += 1

    def add_alias(
            self,
            alias: str
    ) -> None:
        alias = alias.strip()
        if alias and alias not in self.aliases:
            self.aliases.append(alias)
            self.touch()

    def add_tag(
            self,
            tag: str
    ) -> None:
        tag = tag.strip().lower()
        if tag and tag not in self.tags:
            self.tags.append(tag)
            self.touch()

    def set_metadata(
            self,
            key: str,
            value: Any
    ) -> None:
        self.metadata[key] = value
        self.touch()

    def get_metadata(
            self,
            key: str,
            default=None
    ):
        return self.metadata.get(
            key,
            default
        )

    def rename(
            self,
            title: str
    ) -> None:
        self.title = title.strip()
        self.touch()

    def publish(self) -> None:
        self.status = EntityStatus.PUBLISHED
        self.touch()

    def archive(self) -> None:
        self.status = EntityStatus.ARCHIVED
        self.touch()

    def verify(self) -> None:
        self.status = EntityStatus.VERIFIED
        self.confidence = ConfidenceLevel.VERIFIED
        self.touch()

    @property
    def is_published(self) -> bool:
        return (
                self.status
                ==
                EntityStatus.PUBLISHED
        )

    @property
    def is_verified(self) -> bool:
        return (
                self.status
                ==
                EntityStatus.VERIFIED
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type.value,
            "title": self.title,
            "code": self.code,
            "description": self.description,
            "aliases": self.aliases,
            "tags": self.tags,
            "metadata": self.metadata,
            "source": self.source.value,
            "status": self.status.value,
            "confidence": self.confidence.value,
            "version": self.version,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "entity_type": self.entity_type.value,
            "slug": self.slug,
            "attributes": self.attributes
        }

    def __repr__(self):
        return (
            f"<Entity "
            f"{self.type.value}: "
            f"{self.title}>"
        )
