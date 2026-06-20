"""
════════════════════════════════════════════════════════════════════

GENESIS HR®

Knowledge Core

Module:
Entity Registry

File:
entity_serializer.py

Purpose:
Serialization and deserialization of Entity objects.

════════════════════════════════════════════════════════════════════
"""

from datetime import datetime

from .entity import Entity
from .enums import ConfidenceLevel
from .enums import EntitySource
from .enums import EntityStatus
from .enums import EntityType


class EntitySerializer:

    @staticmethod
    def to_dict(
        entity: Entity
    ) -> dict:

        return {

            "id": entity.id,

            "type": entity.type.value,

            "title": entity.title,

            "code": entity.code,

            "description": entity.description,

            "aliases": entity.aliases,

            "tags": entity.tags,

            "metadata": entity.metadata,

            "source": entity.source.value,

            "status": entity.status.value,

            "confidence": entity.confidence.value,

            "version": entity.version,

            "created_at": entity.created_at.isoformat(),

            "updated_at": entity.updated_at.isoformat()

        }

    @staticmethod
    def from_dict(
        data: dict
    ) -> Entity:

        entity = Entity(

            id=data["id"],

            type=EntityType(
                data["type"]
            ),

            title=data["title"],

            code=data.get(
                "code"
            ),

            description=data.get(
                "description",
                ""
            ),

            aliases=data.get(
                "aliases",
                []
            ),

            tags=data.get(
                "tags",
                []
            ),

            metadata=data.get(
                "metadata",
                {}
            ),

            source=EntitySource(
                data.get(
                    "source",
                    "manual"
                )
            ),

            status=EntityStatus(
                data.get(
                    "status",
                    "draft"
                )
            ),

            confidence=ConfidenceLevel(
                data.get(
                    "confidence",
                    "unknown"
                )
            )

        )

        entity.version = data.get(
            "version",
            1
        )

        if "created_at" in data:

            entity.created_at = datetime.fromisoformat(
                data["created_at"]
            )

        if "updated_at" in data:

            entity.updated_at = datetime.fromisoformat(
                data["updated_at"]
            )

        return entity