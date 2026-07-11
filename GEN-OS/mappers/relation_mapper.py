"""
===============================================================================

 GENESIS HR®
 GEN-OS

 FILE
 ----
 mappers/relation_mapper.py

 BUILD
 -----
 0.2.1

 DESCRIPTION
 -----------
 Universal Relation Mapper.

 Creates KnowledgeEdge objects from
 ESCO and O*NET datasets.

===============================================================================
"""

from __future__ import annotations

from typing import Any
from typing import Iterable

from models.knowledge_edge import KnowledgeEdge


class RelationMapper:
    """
    Maps external dataset relations
    into Knowledge Graph edges.
    """

    # ------------------------------------------------------------------

    @staticmethod
    def profession_skill(
        row: dict[str, Any]
    ) -> KnowledgeEdge:
        """
        ESCO occupation -> skill
        """

        return KnowledgeEdge(

            source=row.get(
                "occupationUri",
                ""
            ),

            target=row.get(
                "skillUri",
                ""
            ),

            relation=row.get(
                "relationType",
                "HAS_SKILL"
            ),

            weight=1.0,

            bidirectional=False

        )

    # ------------------------------------------------------------------

    @staticmethod
    def profession_competency(
        profession_id: str,
        competency_id: str
    ) -> KnowledgeEdge:

        return KnowledgeEdge(

            source=profession_id,

            target=competency_id,

            relation="HAS_COMPETENCY",

            weight=1.0,

            bidirectional=False

        )

    # ------------------------------------------------------------------

    @staticmethod
    def skill_competency(
        skill_id: str,
        competency_id: str
    ) -> KnowledgeEdge:

        return KnowledgeEdge(

            source=skill_id,

            target=competency_id,

            relation="REQUIRES",

            weight=1.0,

            bidirectional=False

        )

    # ------------------------------------------------------------------

    @staticmethod
    def profession_course(
        profession_id: str,
        course_id: str
    ) -> KnowledgeEdge:

        return KnowledgeEdge(

            source=profession_id,

            target=course_id,

            relation="LEARN_BY",

            weight=0.8

        )

    # ------------------------------------------------------------------

    @staticmethod
    def profession_vacancy(
        profession_id: str,
        vacancy_id: str
    ) -> KnowledgeEdge:

        return KnowledgeEdge(

            source=profession_id,

            target=vacancy_id,

            relation="HAS_VACANCY",

            weight=1.0

        )

    # ------------------------------------------------------------------

    @staticmethod
    def occupation_collection(
        rows: Iterable[dict]
    ) -> list[KnowledgeEdge]:

        return [

            RelationMapper.profession_skill(row)

            for row in rows

        ]
    # ------------------------------------------------------------------

    @staticmethod
    def profession_skill_edges(
        profession_id: str,
        skill_ids: Iterable[str]
    ) -> list[KnowledgeEdge]:
        """
        Build Profession -> Skill edges.
        """

        return [

            KnowledgeEdge(

                source=profession_id,

                target=skill,

                relation="HAS_SKILL",

                weight=1.0,

                bidirectional=False

            )

            for skill in skill_ids

        ]

    # ------------------------------------------------------------------

    @staticmethod
    def skill_competency_edges(
        skill_id: str,
        competency_ids: Iterable[str]
    ) -> list[KnowledgeEdge]:
        """
        Build Skill -> Competency edges.
        """

        return [

            KnowledgeEdge(

                source=skill_id,

                target=competency,

                relation="REQUIRES",

                weight=1.0,

                bidirectional=False

            )

            for competency in competency_ids

        ]

    # ------------------------------------------------------------------

    @staticmethod
    def profession_course_edges(
        profession_id: str,
        course_ids: Iterable[str]
    ) -> list[KnowledgeEdge]:
        """
        Build Profession -> Course edges.
        """

        return [

            KnowledgeEdge(

                source=profession_id,

                target=course,

                relation="CAN_BE_LEARNED_BY",

                weight=0.85,

                bidirectional=False

            )

            for course in course_ids

        ]

    # ------------------------------------------------------------------

    @staticmethod
    def profession_vacancy_edges(
        profession_id: str,
        vacancy_ids: Iterable[str]
    ) -> list[KnowledgeEdge]:
        """
        Build Profession -> Vacancy edges.
        """

        return [

            KnowledgeEdge(

                source=profession_id,

                target=vacancy,

                relation="HAS_VACANCY",

                weight=1.0,

                bidirectional=False

            )

            for vacancy in vacancy_ids

        ]

    # ------------------------------------------------------------------

    @staticmethod
    def reverse(
        edge: KnowledgeEdge
    ) -> KnowledgeEdge:
        """
        Create reverse edge.
        """

        return KnowledgeEdge(

            source=edge.target,

            target=edge.source,

            relation=edge.relation,

            weight=edge.weight,

            bidirectional=edge.bidirectional

        )

    # ------------------------------------------------------------------

    @staticmethod
    def bidirectional(
        edge: KnowledgeEdge
    ) -> list[KnowledgeEdge]:
        """
        Return forward + reverse edges.
        """

        return [

            edge,

            RelationMapper.reverse(edge)

        ]

    # ------------------------------------------------------------------

    @staticmethod
    def unique(
        edges: Iterable[KnowledgeEdge]
    ) -> list[KnowledgeEdge]:
        """
        Remove duplicate edges.
        """

        result = []

        visited = set()

        for edge in edges:

            key = (

                edge.source,

                edge.target,

                edge.relation

            )

            if key in visited:

                continue

            visited.add(key)

            result.append(edge)

        return result

    # ------------------------------------------------------------------

    @staticmethod
    def statistics(
        edges: Iterable[KnowledgeEdge]
    ) -> dict:
        """
        Graph edge statistics.
        """

        edges = list(edges)

        relations = {}

        for edge in edges:

            relations.setdefault(

                edge.relation,

                0

            )

            relations[edge.relation] += 1

        return {

            "edges": len(edges),

            "relation_types": len(relations),

            "relations": relations

        }

    # ------------------------------------------------------------------

    @staticmethod
    def validate(
        edge: KnowledgeEdge
    ) -> bool:
        """
        Validate graph edge.
        """

        return bool(

            edge.source

            and edge.target

            and edge.relation

        )
