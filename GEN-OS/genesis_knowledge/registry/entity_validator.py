"""
════════════════════════════════════════════════════════════════════

GENESIS HR®

Knowledge Core

Module:
Entity Registry

File:
entity_validator.py

Purpose:
Validates entities before they enter the Knowledge Registry.

════════════════════════════════════════════════════════════════════
"""

from typing import List

from .entity import Entity


class EntityValidator:

    MIN_TITLE_LENGTH = 2

    MAX_TITLE_LENGTH = 255

    @classmethod
    def validate(
        cls,
        entity: Entity
    ) -> List[str]:

        errors = []

        errors.extend(
            cls.validate_title(entity)
        )

        errors.extend(
            cls.validate_code(entity)
        )

        errors.extend(
            cls.validate_aliases(entity)
        )

        errors.extend(
            cls.validate_tags(entity)
        )

        return errors

    @classmethod
    def validate_title(
        cls,
        entity: Entity
    ) -> List[str]:

        errors = []

        title = entity.title.strip()

        if not title:

            errors.append(
                "Title is required."
            )

            return errors

        if len(title) < cls.MIN_TITLE_LENGTH:

            errors.append(
                "Title is too short."
            )

        if len(title) > cls.MAX_TITLE_LENGTH:

            errors.append(
                "Title is too long."
            )

        return errors

    @classmethod
    def validate_code(
        cls,
        entity: Entity
    ) -> List[str]:

        errors = []

        if entity.code is None:

            return errors

        if len(entity.code.strip()) == 0:

            errors.append(
                "Code cannot be empty."
            )

        return errors

    @classmethod
    def validate_aliases(
        cls,
        entity: Entity
    ) -> List[str]:

        errors = []

        aliases = set()

        for alias in entity.aliases:

            value = alias.strip().lower()

            if not value:

                errors.append(
                    "Alias cannot be empty."
                )

                continue

            if value in aliases:

                errors.append(
                    f"Duplicate alias: {alias}"
                )

            aliases.add(value)

        return errors

    @classmethod
    def validate_tags(
        cls,
        entity: Entity
    ) -> List[str]:

        errors = []

        tags = set()

        for tag in entity.tags:

            value = tag.strip().lower()

            if not value:

                errors.append(
                    "Empty tag detected."
                )

                continue

            if value in tags:

                errors.append(
                    f"Duplicate tag: {tag}"
                )

            tags.add(value)

        return errors

    @classmethod
    def is_valid(
        cls,
        entity: Entity
    ) -> bool:

        return len(
            cls.validate(entity)
        ) == 0
