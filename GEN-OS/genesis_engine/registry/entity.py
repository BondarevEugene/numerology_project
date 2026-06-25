"""
═══════════════════════════════════════════════════════════════════════
MODULE ID:     GKH-REG-000
NAME:          Genesis Entity
LAYER:         Knowledge Registry
VERSION:       2.0.0 Alpha

DESCRIPTION

Universal knowledge object.
Everything inside Genesis
is represented by Entity.

Profession
Competency
Habit
Book
Sport
Protocol
Environment
Technology
...

Nothing exists outside Entity.
═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass
from dataclasses import field

from datetime import datetime

from typing import Dict
from typing import List
from typing import Any

from uuid import uuid4

from ..schema.knowledge_schema import EntityType


@dataclass
class Entity:
    # ==========================================================
    # IDENTIFICATION
    # ==========================================================
    uuid: str
    type: EntityType
    code: str
    slug: str
    # ==========================================================
    # TITLES
    # ==========================================================
    title: str
    title_ru: str = ""
    title_ua: str = ""
    aliases: List[str] = field(default_factory=list)
    # ==========================================================
    # DESCRIPTION
    # ==========================================================
    description: str = ""
    short_description: str = ""
    # ==========================================================
    # CLASSIFICATION
    # ==========================================================
    category: str = ""
    subcategory: str = ""
    tags: List[str] = field(default_factory=list)
    # ==========================================================
    # STATE
    # ==========================================================
    source: str = ""
    status: str = "draft"
    language: str = "en"
    confidence: float = 1.0
    # ==========================================================
    # DYNAMIC ATTRIBUTES
    # ==========================================================
    attributes: Dict[str, Any] = field(
        default_factory=dict
    )
    metadata: Dict[str, Any] = field(
        default_factory=dict
    )
    passport: Dict[str, Any] = field(
        default_factory=dict
    )
    # ==========================================================
    # AUDIT
    # ==========================================================
    created_at: datetime = field(
        default_factory=datetime.utcnow
    )
    updated_at: datetime = field(
        default_factory=datetime.utcnow
    )
    version: str = "1.0"

    # ==========================================================
    # SERIALIZATION
    # ==========================================================

    def to_dict(self):
        return {

            "uuid": self.uuid,
            "type": self.type.value,
            "code": self.code,
            "slug": self.slug,
            "title": self.title,
            "title_ru": self.title_ru,
            "title_ua": self.title_ua,
            "aliases": self.aliases,
            "description": self.description,
            "short_description": self.short_description,
            "category": self.category,
            "subcategory": self.subcategory,
            "tags": self.tags,
            "source": self.source,
            "status": self.status,
            "language": self.language,
            "confidence": self.confidence,
            "attributes": self.attributes,
            "metadata": self.metadata,
            "passport": self.passport,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "version": self.version
        }

    # ==========================================================
    # ATTRIBUTE HELPERS
    # ==========================================================

    def get(self, key, default=None):
        return self.attributes.get(
            key,
            default
        )

    def set(self, key, value):
        self.attributes[key] = value

    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def add_alias(self, alias):
        if alias not in self.aliases:
            self.aliases.append(alias)

    # ==========================================================
    # PASSPORT
    # ==========================================================
    def provider(self):
        return self.passport.get(
            "provider"
        )

    def import_batch(self):
        return self.passport.get(
            "import_batch"
        )

    def external_id(self):
        return self.passport.get(
            "external_id"
        )

    # ==========================================================
    # DEBUG
    # ==========================================================

    def __repr__(self):
        return (
            f"<Entity "
            f"{self.type.value}: "
            f"{self.title}>"
        )
