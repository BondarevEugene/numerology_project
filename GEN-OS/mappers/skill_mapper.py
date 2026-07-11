"""
===============================================================================
 GENESIS HR®  GEN-OS
 FILE ---- mappers/skill_mapper.py
 DESCRIPTION
 -----------
 Universal Skill mapper.
===============================================================================
"""

from __future__ import annotations
from typing import Any
from models.skill import Skill


class SkillMapper:

    # ------------------------------------------------------------------

    @staticmethod
    def from_esco(row: dict[str, Any]
    ) -> Skill:
        skill = Skill(
            id=row.get(
                "conceptUri",
                ""
            ),
            name=row.get(
                "preferredLabel",
                ""
            ),
            category=row.get(
                "skillType",
                "General"
            ),
            description=row.get(
                "description",
                ""
            )
        )
        skill.metadata = {
            "provider": "ESCO",
            "reuseLevel": row.get(
                "reuseLevel"
            ),
            "status": row.get(
                "status"
            )
        }
        return skill
    # ------------------------------------------------------------------

    @staticmethod
    def from_onet(row: dict[str, Any]) -> Skill:
        skill = Skill(
            id=row.get(
                "Element ID",
                ""
            ),
            name=row.get(
                "Element Name",
                ""
            ),
            category=row.get(
                "Scale ID",
                "General"
            ),
            description=""
        )

        skill.metadata = {
            "provider": "ONET",
            "scale": row.get(
                "Scale ID"),
            "importance": row.get(
                "Data Value"
            )
        }
        return skill

    # ------------------------------------------------------------------

    @staticmethod
    def collection_from_esco(rows) -> list[Skill]:
        return [
            SkillMapper.from_esco(row)
            for row in rows
        ]

    # ------------------------------------------------------------------

    @staticmethod
    def collection_from_onet(rows) -> list[Skill]:
        return [
            SkillMapper.from_onet(row)
            for row in rows
        ]
    # ------------------------------------------------------------------

    @staticmethod
    def merge(esco: Skill, onet: Skill) -> Skill:
        """
        Merge ESCO and O*NET skill.

        ESCO is primary.
        O*NET enriches metadata.
        """
        if not esco.description:
            esco.description = onet.description
        esco.tags.extend(
            tag
            for tag in onet.tags
            if tag not in esco.tags
        )
        esco.professions.extend(
            profession
            for profession in onet.professions
            if profession not in esco.professions
        )
        esco.competencies.extend(
            competency
            for competency in onet.competencies
            if competency not in esco.competencies
        )
        esco.metadata.update(
            onet.metadata
        )
        return esco

    # ------------------------------------------------------------------

    @staticmethod
    def normalize(skill: Skill) -> Skill:
        """
        Normalize object.
        """
        skill.name = skill.name.strip()
        skill.category = skill.category.strip()
        skill.description = (skill.description.strip())
        skill.tags = sorted(set(skill.tags))
        skill.professions = sorted(set(skill.professions))
        skill.competencies = sorted(set(skill.competencies))
        return skill

    # ------------------------------------------------------------------

    @staticmethod
    def validate(skill: Skill) -> bool:
        """
        Validate model.
        """
        return bool(skill.id and skill.name)

    # ------------------------------------------------------------------

    @staticmethod
    def index(skills: list[Skill]) -> dict[str, Skill]:
        """
        Build lookup dictionary.
        """
        return {
            skill.id: skill
            for skill in skills
        }
