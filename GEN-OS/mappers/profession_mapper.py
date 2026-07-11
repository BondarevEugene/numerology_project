"""
===============================================================================

 GENESIS HR® GEN-OS

 FILE ---- mappers/profession_mapper.py

 BUILD ----- 0.2.1

 DESCRIPTION
 -----------
 Maps ESCO / O*NET occupation records
 into GEN-OS Profession objects.
===============================================================================
"""

from __future__ import annotations
from typing import Any
from models.profession import Profession


class ProfessionMapper:
    """
    Universal Profession mapper.
    Supports
        • ESCO
        • O*NET
        • Future Providers
    """
    # ------------------------------------------------------------------

    @staticmethod
    def from_esco(
        row: dict[str, Any]
    ) -> Profession:
        """
        Convert ESCO occupation
        into Profession.
        """
        profession = Profession(
            id=row.get("conceptUri", ""),
            name=row.get(
                "preferredLabel",
                ""
            ),
            category=row.get(
                "iscoGroup",
                "General"
            ),
            description=row.get(
                "description",
                ""
            ),
        )

        profession.metadata = {
            "provider": "ESCO",
            "uri": row.get(
                "conceptUri"
            ),
            "code": row.get(
                "code"
            ),
            "status": row.get(
                "status"
            )
        }

        return profession

    # ------------------------------------------------------------------

    @staticmethod
    def from_onet(
        row: dict[str, Any]
    ) -> Profession:
        """
        Convert O*NET occupation
        into Profession.
        """
        profession = Profession(
            id=row.get(
                "O*NET-SOC Code",
                ""
            ),
            name=row.get(
                "Title",
                ""
            ),
            category=row.get(
                "Job Zone",
                "General"
            ),
            description=row.get(
                "Description",
                ""
            )
        )

        profession.metadata = {
            "provider": "ONET",
            "soc": row.get(
                "O*NET-SOC Code"
            )
        }

        return profession
    # ------------------------------------------------------------------

    @staticmethod
    def collection_from_esco(
        rows
    ) -> list[Profession]:
        """
        Convert iterable.
        """
        return [
            ProfessionMapper.from_esco(
                row
            )
            for row in rows
        ]
    # ------------------------------------------------------------------

    @staticmethod
    def collection_from_onet(
        rows
    ) -> list[Profession]:
        return [
            ProfessionMapper.from_onet(
                row
            )
            for row in rows
        ]
    # ------------------------------------------------------------------

    @staticmethod
    def merge(esco: Profession, onet: Profession) -> Profession:
        """
        Merge ESCO and O*NET profession.

        ESCO is considered the primary source,
        O*NET enriches the model.
        """
        if not esco.description:
            esco.description = onet.description
        esco.tags.extend(
            tag
            for tag in onet.tags
            if tag not in esco.tags
        )
        esco.metadata.update(
            onet.metadata
        )
        return esco

    # ------------------------------------------------------------------

    @staticmethod
    def normalize(
        profession: Profession
    ) -> Profession:
        """
        Normalize values.
        """
        profession.name = profession.name.strip()
        profession.category = profession.category.strip()
        profession.description = (
            profession.description.strip()
        )
        profession.tags = sorted(
            set(profession.tags)
        )
        profession.skills = sorted(
            set(profession.skills)
        )
        profession.competencies = sorted(
            set(profession.competencies)
        )
        return profession
    # ------------------------------------------------------------------

    @staticmethod
    def index(
        professions: list[Profession]
    ) -> dict[str, Profession]:
        """
        Build lookup dictionary.
        """
        return {
            profession.id: profession
            for profession in professions
        }

    # ------------------------------------------------------------------

    @staticmethod
    def validate(
        profession: Profession
    ) -> bool:
        """
        Minimal validation.
        """
        return bool(
            profession.id
            and profession.name
        )
