"""
===============================================================================

GENESIS HR®

Profession Repository

Knowledge Repository

BUILD 0201

===============================================================================
"""

from __future__ import annotations

from repositories.base_repository import BaseRepository

from models.profession import Profession

from services.knowledge_graph_service import (
    knowledge_graph
)


class ProfessionRepository(
    BaseRepository[Profession]
):

    """
    Enterprise Profession Repository.
    """

    # ------------------------------------------------------------

    def by_category(
        self,
        category: str
    ) -> list[Profession]:

        return self.filter(

            lambda p:

            p.category.lower()

            == category.lower()

        )

    # ------------------------------------------------------------

    def by_skill(
        self,
        skill_id: str
    ) -> list[Profession]:

        result = []

        for profession in self:

            if skill_id in profession.skills:

                result.append(
                    profession
                )

        return result

    # ------------------------------------------------------------

    def related(
        self,
        profession_id: str
    ) -> list[Profession]:
        """
        Graph neighbours.
        """

        neighbours = knowledge_graph.neighbours(
            profession_id
        )

        return [

            node

            for node in neighbours

            if isinstance(
                node,
                Profession
            )

        ]

    # ------------------------------------------------------------

    def required_skills(
        self,
        profession_id: str
    ) -> list[str]:

        profession = self.get(
            profession_id
        )

        if profession is None:

            return []

        return sorted(

            profession.skills

        )

    # ------------------------------------------------------------

    def competencies(
        self,
        profession_id: str
    ) -> list[str]:

        profession = self.get(
            profession_id
        )

        if profession is None:

            return []

        return sorted(

            profession.competencies

        )
    # ------------------------------------------------------------
    # GRAPH
    # ------------------------------------------------------------

    def neighbour_skills(
        self,
        profession_id: str
    ):
        """
        Return Skill nodes connected
        with profession.
        """

        from models.skill import Skill

        return [

            node

            for node in knowledge_graph.neighbours(
                profession_id
            )

            if isinstance(node, Skill)

        ]

    # ------------------------------------------------------------

    def neighbour_courses(
        self,
        profession_id: str
    ):
        """
        Return Course nodes.
        """

        from models.course import Course

        return [

            node

            for node in knowledge_graph.neighbours(
                profession_id
            )

            if isinstance(node, Course)

        ]

    # ------------------------------------------------------------

    def neighbour_vacancies(
        self,
        profession_id: str
    ):
        """
        Return Vacancy nodes.
        """

        from models.vacancy import Vacancy

        return [

            node

            for node in knowledge_graph.neighbours(
                profession_id
            )

            if isinstance(node, Vacancy)

        ]

    # ------------------------------------------------------------

    def career_path(
        self,
        source_id: str,
        target_id: str
    ) -> list[Profession]:
        """
        Find career path between
        two professions.
        """

        ids = knowledge_graph.shortest_path(

            source_id,

            target_id

        )

        result = []

        for profession_id in ids:

            profession = self.get(
                profession_id
            )

            if profession is not None:

                result.append(
                    profession
                )

        return result

    # ------------------------------------------------------------

    def similar(
        self,
        profession_id: str
    ) -> list[Profession]:
        """
        Similar professions.

        Currently graph neighbours.

        Future:

            Graph similarity

            AI embeddings

            Skill overlap
        """

        return self.related(
            profession_id
        )

    # ------------------------------------------------------------

    def by_tag(
        self,
        tag: str
    ) -> list[Profession]:

        return self.find_by_tag(
            tag
        )

    # ------------------------------------------------------------

    def enabled(
        self
    ) -> list[Profession]:

        return self.filter(

            lambda p:

            p.enabled

        )

    # ------------------------------------------------------------

    def disabled(
        self
    ) -> list[Profession]:

        return self.filter(

            lambda p:

            not p.enabled

        )

    # ------------------------------------------------------------

    def statistics(
        self
    ) -> dict:

        stats = super().statistics()

        stats["categories"] = len({

            p.category

            for p in self

        })

        return stats

        # ------------------------------------------------------------

        def dashboard(
                self
        ) -> dict:
            """
            Dashboard statistics
            for workspace.
            """

            stats = self.statistics()

            stats["top_categories"] = {}

            for profession in self:
                stats["top_categories"].setdefault(

                    profession.category,

                    0

                )

                stats["top_categories"][
                    profession.category
                ] += 1

            return stats

        # ------------------------------------------------------------

        def export(
                self
        ) -> list[dict]:
            return self.to_dict()

        # ------------------------------------------------------------

        def __repr__(self):
            return (

                "<ProfessionRepository "

                f"count={self.count()}>"

            )

    # ============================================================
    # GLOBAL INSTANCE
    # ============================================================

    profession_repository = ProfessionRepository()
