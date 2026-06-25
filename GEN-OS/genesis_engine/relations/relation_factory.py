"""
═══════════════════════════════════════════════════════════════════════
GENESIS KNOWLEDGE ENGINE
MODULE    Relation Factory
MODULE ID    GKH-REL-002
VERSION    1.0.0 Alpha
LAYER    Knowledge Graph

DESCRIPTION
Creates every Relation inside Genesis.
Nothing creates Relation directly.
Every graph connection MUST be created
through RelationFactory.
═══════════════════════════════════════════════════════════════════════
"""

from uuid import uuid4
from .relation import Relation


class RelationFactory:

    # ==========================================================
    # BASE
    # ==========================================================

    @staticmethod
    def create(
            source,
            target,
            relation_type,
            weight=1.0,
            confidence=1.0,
            bidirectional=False,
            source_name="manual",
            metadata=None
    ):
        if metadata is None:
            metadata = {}
        return Relation(
            uuid=str(uuid4()),
            source_uuid=source.uuid,
            target_uuid=target.uuid,
            relation_type=relation_type,
            weight=weight,
            confidence=confidence,
            bidirectional=bidirectional,
            source=source_name,
            metadata=metadata
        )

    # ==========================================================
    # PROFESSION
    # ==========================================================

    @staticmethod
    def requires(
            profession,
            competency,
            weight=1.0
    ):
        return RelationFactory.create(
            profession,
            competency,
            "requires",
            weight
        )

    @staticmethod
    def recommended_book(
            entity,
            book,
            weight=1.0
    ):
        return RelationFactory.create(
            entity,
            book,
            "recommended_book",
            weight
        )

    @staticmethod
    def develops(
            source,
            target,
            weight=1.0
    ):
        return RelationFactory.create(
            source,
            target,
            "develops",
            weight
        )

    @staticmethod
    def improves(
            source,
            target,
            weight=1.0
    ):
        return RelationFactory.create(
            source,
            target,
            "improves",
            weight
        )

    @staticmethod
    def weakens(
            source,
            target,
            weight=1.0
    ):
        return RelationFactory.create(
            source,
            target,
            "weakens",
            weight
        )

    @staticmethod
    def suitable_for(
            source,
            target,
            weight=1.0
    ):
        return RelationFactory.create(
            source,
            target,
            "suitable_for",
            weight
        )

    @staticmethod
    def opposite(
            source,
            target
    ):
        return RelationFactory.create(
            source,
            target,
            "opposite"
        )

    @staticmethod
    def similar(
            source,
            target
    ):
        return RelationFactory.create(
            source,
            target,
            "similar"
        )

    @staticmethod
    def parent(
            source,
            target
    ):
        return RelationFactory.create(
            source,
            target,
            "parent"
        )

    @staticmethod
    def child(
            source,
            target
    ):
        return RelationFactory.create(
            source,
            target,
            "child"
        )
