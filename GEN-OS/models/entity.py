"""
═══════════════════════════════════════════════════════════════════════

GENESIS®

Universal Entity

BUILD 0104

Every object inside GENESIS is an Entity.

═══════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime
from typing import Any


@dataclass
class Entity:

    id: str = field(default_factory=lambda: str(uuid4()))

    type: str = "entity"

    name: str = ""

    title: str = ""

    description: str = ""

    version: str = "1.0"

    enabled: bool = True

    created_at: datetime = field(default_factory=datetime.utcnow)

    updated_at: datetime = field(default_factory=datetime.utcnow)

    tags: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    attributes: dict[str, Any] = field(default_factory=dict)

    relations: list[str] = field(default_factory=list)

    def touch(self):

        self.updated_at = datetime.utcnow()

    def add_tag(self, tag: str):

        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str):

        if tag in self.tags:
            self.tags.remove(tag)

    def set(self, key: str, value: Any):

        self.attributes[key] = value

        self.touch()

    def get(self, key: str, default=None):

        return self.attributes.get(key, default)

    def add_relation(self, relation_id: str):

        if relation_id not in self.relations:
            self.relations.append(relation_id)

    def to_dict(self):

        return {

            "id": self.id,

            "type": self.type,

            "name": self.name,

            "title": self.title,

            "description": self.description,

            "version": self.version,

            "enabled": self.enabled,

            "created_at": self.created_at.isoformat(),

            "updated_at": self.updated_at.isoformat(),

            "tags": self.tags,

            "metadata": self.metadata,

            "attributes": self.attributes,

            "relations": self.relations,

        }