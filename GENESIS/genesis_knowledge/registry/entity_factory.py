"""
═══════════════════════════════════════════════════════════════════════

MODULE ID:     GKH-REG-001
NAME:     Entity Factory
LAYER:     Knowledge Registry
VERSION:    0.1.0 Alpha
STATUS:    Stable
PURPOSE

Universal constructor of every knowledge entity.

Every Provider.
Every Importer.
Every AI Generator.

MUST use EntityFactory.

No Entity is created manually.

RESPONSIBILITIES

✓ Generate UUID
✓ Generate Code
✓ Build Entity
✓ Create Passport
✓ Attach Attributes
✓ Attach Metadata
✓ Normalize defaults

ROADMAP

v1.0     Basic Factory
v1.1     Validation hooks
v1.2     Event Bus
v2.0     Auto Graph Registration
══════════════════════════════════════════════════════════════════════════════
"""

from uuid import uuid4

from slugify import slugify

from .entity import Entity

from ..schema.knowledge_schema import (
    EntityType,
    SourceType,
    EntityStatus
)


class EntityFactory:
    """
    Universal Genesis Entity Builder.
    """

    VERSION = "1.0.0"
    MODULE = "EntityFactory"

    # ==========================================================
    # CORE BUILDER
    # ==========================================================

    @staticmethod
    def build(
        entity_type: EntityType,
        title: str,
        title_ru: str = "",
        title_ua: str = "",
        description: str = "",
        category: str = "",
        subcategory: str = "",
        source: SourceType = SourceType.MANUAL,
        status: EntityStatus = EntityStatus.DRAFT,
        aliases=None,
        attributes=None,
        metadata=None,
        passport=None,
        code=None
    ):

        if aliases is None:
            aliases = []

        if attributes is None:
            attributes = {}

        if metadata is None:
            metadata = {}

        if passport is None:
            passport = {}

        if code is None:
            code = slugify(title)

        attributes.setdefault(
            "category",
            category
        )

        attributes.setdefault(
            "subcategory",
            subcategory
        )

        passport.setdefault(
            "provider",
            source.value
        )

        passport.setdefault(
            "provider_version",
            "1.0"
        )

        passport.setdefault(
            "import_batch",
            None
        )

        passport.setdefault(
            "external_id",
            None
        )

        entity = Entity(
            uuid=str(uuid4()),
            type=entity_type,
            code=code,
            title=title,
            title_ru=title_ru,
            title_ua=title_ua,
            description=description,
            source=source.value,
            status=status.value,
            attributes=attributes,
            metadata=metadata,
            passport=passport
        )

        print(
            f"[ENTITY FACTORY] "
            f"{entity_type.value.upper()} "
            f"created -> {title}"
        )

        return entity

    # ==========================================================
    # SHORTCUTS
    # ==========================================================

    @staticmethod
    def profession(**kwargs):
        return EntityFactory.build(
            EntityType.PROFESSION,
            **kwargs
        )

    @staticmethod
    def competency(**kwargs):
        return EntityFactory.build(
            EntityType.COMPETENCY,
            **kwargs
        )

    @staticmethod
    def habit(**kwargs):
        return EntityFactory.build(
            EntityType.HABIT,
            **kwargs
        )

    @staticmethod
    def hobby(**kwargs):
        return EntityFactory.build(
            EntityType.HOBBY,
            **kwargs
        )

    @staticmethod
    def sport(**kwargs):
        return EntityFactory.build(
            EntityType.SPORT,
            **kwargs
        )

    @staticmethod
    def book(**kwargs):
        return EntityFactory.build(
            EntityType.BOOK,
            **kwargs
        )

    @staticmethod
    def protocol(**kwargs):
        return EntityFactory.build(
            EntityType.PROTOCOL,
            **kwargs
        )

    @staticmethod
    def behavior(**kwargs):
        return EntityFactory.build(
            EntityType.BEHAVIOR,
            **kwargs
        )

    @staticmethod
    def environment(**kwargs):
        return EntityFactory.build(
            EntityType.ENVIRONMENT,
            **kwargs
        )

    @staticmethod
    def career(**kwargs):
        return EntityFactory.build(
            EntityType.CAREER_PATH,
            **kwargs
        )