"""
===============================================================================
 GENESIS HR® Skill Repository

 BUILD 0202
 DESCRIPTION
 -----------
 Central repository for every Skill inside GEN-OS.
===============================================================================
"""

from __future__ import annotations
from repositories.base_repository import BaseRepository
from models.skill import Skill
from services.knowledge_graph_service import (knowledge_graph)


class SkillRepository(
    BaseRepository[Skill]
):
    """
    Enterprise Skill Repository.
    """

    # ------------------------------------------------------------

    def by_category(
            self,
            category: str
    ) -> list[Skill]:
        return self.filter(
            lambda s:
            s.category.lower()
            == category.lower()
        )

    # ------------------------------------------------------------

    def professions(self, skill_id: str):
        """
        Return professions using skill.
        """
        from models.profession import Profession
        return [
            node
            for node in knowledge_graph.parents(
                skill_id
            )
            if isinstance(
                node,
                Profession
            )
        ]

    # ------------------------------------------------------------

    def competencies(self, skill_id: str):
        """
        Skill competencies.
        """
        from models.competency import Competency
        return [node for node in knowledge_graph.neighbours(skill_id)
                if isinstance(node, Competency)]

    # ------------------------------------------------------------

    def courses(
            self,
            skill_id: str
    ):
        from models.course import Course
        return [
            node
            for node in knowledge_graph.neighbours(
                skill_id
            )
            if isinstance(
                node,
                Course
            )
        ]

    # ------------------------------------------------------------

    def vacancies(self, skill_id: str):
        from models.vacancy import Vacancy
        return [
            node
            for node in knowledge_graph.parents(
                skill_id
            )
            if isinstance(
                node,
                Vacancy
            )
        ]

    # ------------------------------------------------------------

    def related(self, skill_id: str):
        from models.skill import Skill
        return [node for node in knowledge_graph.connected_nodes(skill_id)
            if isinstance(node, Skill)]

    # ------------------------------------------------------------
    # RECOMMENDATIONS
    # ------------------------------------------------------------

    def recommend_professions(
            self,
            skill_id: str
    ):
        """
        Alias for professions().
        Future:
            Ranking
            AI Scoring
            Market weighting
        """
        return self.professions(
            skill_id
        )

    # ------------------------------------------------------------

    def recommend_courses(
            self,
            skill_id: str
    ):
        """
        Courses teaching this skill.
        """
        return self.courses(
            skill_id
        )

    # ------------------------------------------------------------

    def learning_path(
            self,
            skill_id: str
    ):
        """
        Ordered learning path.
        Current implementation:
            Competencies
                ↓
            Courses
        """
        return {
            "skill": self.get(
                skill_id
            ),
            "competencies":
                self.competencies(
                    skill_id
                ),
            "courses":

                self.courses(
                    skill_id
                )
        }

    # ------------------------------------------------------------

    def market_demand(self, skill_id: str) -> float:
        """
        Placeholder.
        Future:
            Vacancy statistics
            LinkedIn
            O*NET
            WorkUA
            Djinni
        """
        vacancies = self.vacancies(skill_id)
        return float(len(vacancies))

    # ------------------------------------------------------------

    def salary_impact(self, skill_id: str) -> float:
        """
        Placeholder.
            Future implementation
        will aggregate salaries
        from VacancyRepository.
        """

        vacancies = self.vacancies(skill_id)
        if not vacancies:
            return 0.0
        salaries = []
        for vacancy in vacancies:
            salary = getattr(
                vacancy,
                "salary_max",
                0
            )
            if salary > 0:
                salaries.append(
                    salary
                )
        if not salaries:
            return 0.0
        return sum(
            salaries
        ) / len(salaries)

    # ------------------------------------------------------------

    def popularity(
            self,
            skill_id: str
    ) -> int:
        """
        Popularity based on
        connected professions.
        """

        return len(

            self.professions(
                skill_id
            )

        )

    # ------------------------------------------------------------

    def similar(
            self,
            skill_id: str
    ):
        """
        Similar skills.

        Current:

            Graph neighbours.

        Future:

            Embeddings

            Graph similarity

            AI clustering

        """

        return self.related(
            skill_id
        )

    # ------------------------------------------------------------

    def dashboard(
            self
    ) -> dict:
        """
        Dashboard statistics.
        """

        categories = {}

        for skill in self:
            categories.setdefault(

                skill.category,

                0

            )

            categories[
                skill.category
            ] += 1

        return {

            **self.statistics(),

            "categories":

                categories

        }

        # ------------------------------------------------------------
        # ANALYTICS
        # ------------------------------------------------------------

        def top_skills(
                self,
                limit: int = 20
        ) -> list[Skill]:
            """
            Most demanded skills.

            Ranking is based on the number
            of connected professions.
            """

            return sorted(

                self,

                key=lambda skill:

                self.popularity(skill.id),

                reverse=True

            )[:limit]

        # ------------------------------------------------------------

        def orphan_skills(
                self
        ) -> list[Skill]:
            """
            Skills not connected
            to any profession.
            """

            return [

                skill

                for skill in self

                if self.popularity(skill.id) == 0

            ]

        # ------------------------------------------------------------

        def graph_statistics(
                self
        ) -> dict:
            """
            Skill graph statistics.
            """

            connected = 0

            orphan = 0

            for skill in self:

                if self.popularity(skill.id):

                    connected += 1

                else:

                    orphan += 1

            return {

                "skills": self.count(),

                "connected": connected,

                "orphan": orphan,

                "top":

                    [

                        skill.name

                        for skill in self.top_skills(10)

                    ]

            }

        # ------------------------------------------------------------

        def export(
                self
        ) -> list[dict]:
            """
            Export repository.
            """

            return self.to_dict()

        # ------------------------------------------------------------

        def import_many(
                self,
                skills
        ) -> int:
            """
            Import collection.
            """

            imported = 0

            for skill in skills:
                self.add(skill)

                imported += 1

            return imported

        # ------------------------------------------------------------

        def synchronize_graph(
                self
        ) -> int:
            """
            Ensure every skill exists
            inside KnowledgeGraph.
            """

            added = 0

            for skill in self:

                if knowledge_graph.has_node(
                        skill.id
                ):
                    continue

                knowledge_graph.add_node(
                    skill
                )

                added += 1

            return added

        # ------------------------------------------------------------

        def __repr__(
                self
        ) -> str:

            return (

                "<SkillRepository "

                f"count={self.count()}>"

            )

    # ============================================================
    # GLOBAL INSTANCE
    # ============================================================

    skill_repository = SkillRepository()
