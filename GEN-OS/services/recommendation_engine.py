"""
===============================================================================

 GENESIS HR®

 Recommendation Engine

 BUILD 0301

 DESCRIPTION
 -----------

 Intelligence layer of GEN-OS.

 Responsible for

    • Profession recommendation

    • Skill gap analysis

    • Career path

    • Learning roadmap

    • Vacancy recommendation

===============================================================================
"""

from __future__ import annotations

import logging

from models.profession import Profession
from models.skill import Skill

from repositories.profession_repository import (
    profession_repository
)

from repositories.skill_repository import (
    skill_repository
)

from services.knowledge_graph_service import (
    knowledge_graph
)

LOGGER = logging.getLogger(
    "GEN-OS.RecommendationEngine"
)


class RecommendationEngine:

    """
    Intelligence Engine.

    Works entirely on Knowledge Graph.
    """

    def __init__(self):

        self.professions = profession_repository

        self.skills = skill_repository

        self.graph = knowledge_graph

    # ------------------------------------------------------------

    def profession(
        self,
        profession_id: str
    ) -> Profession | None:

        return self.professions.get(
            profession_id
        )

    # ------------------------------------------------------------

    def skill(
        self,
        skill_id: str
    ) -> Skill | None:

        return self.skills.get(
            skill_id
        )

    # ------------------------------------------------------------

    def recommend_professions(
        self,
        skill_ids: list[str]
    ) -> list[Profession]:
        """
        Recommend professions
        from known skills.
        """

        scores = {}

        for skill_id in skill_ids:

            professions = self.skills.professions(
                skill_id
            )

            for profession in professions:

                scores.setdefault(
                    profession.id,
                    0
                )

                scores[
                    profession.id
                ] += 1

        ranked = sorted(

            scores.items(),

            key=lambda x: x[1],

            reverse=True

        )

        result = []

        for profession_id, _ in ranked:

            profession = self.profession(
                profession_id
            )

            if profession:

                result.append(
                    profession
                )

        return result

    # ------------------------------------------------------------

    def recommend_skills(
        self,
        profession_id: str
    ) -> list[Skill]:
        """
        Skills required
        for profession.
        """

        skills = self.professions.neighbour_skills(
            profession_id
        )

        return sorted(

            skills,

            key=lambda s: s.name

        )
    # ------------------------------------------------------------
    # CAREER ENGINE
    # ------------------------------------------------------------

    def career_path(
        self,
        source_profession: str,
        target_profession: str
    ):
        """
        Find shortest career path
        between two professions.
        """

        ids = self.graph.shortest_path(

            source_profession,

            target_profession

        )

        result = []

        for profession_id in ids:

            profession = self.profession(
                profession_id
            )

            if profession:

                result.append(
                    profession
                )

        return result

    # ------------------------------------------------------------

    def next_skills(
        self,
        profession_id: str,
        user_skill_ids: list[str],
        limit: int = 10
    ):
        """
        Skills that will give the
        greatest increase in profession match.
        """

        report = self.profession_match(

            profession_id,

            user_skill_ids

        )

        missing = report["missing_skills"]

        return missing[:limit]

    # ------------------------------------------------------------

    def learning_plan(
        self,
        profession_id: str,
        user_skill_ids: list[str]
    ) -> dict:
        """
        Build learning roadmap.
        """

        missing = self.next_skills(

            profession_id,

            user_skill_ids

        )

        roadmap = []

        current_score = self.readiness_score(

            profession_id,

            user_skill_ids

        )

        future_score = current_score

        increment = 0

        if missing:

            increment = (

                100.0 - current_score

            ) / len(missing)

        for index, skill in enumerate(missing, start=1):

            future_score = min(

                100.0,

                current_score + increment * index

            )

            roadmap.append({

                "step": index,

                "skill": skill,

                "expected_score": round(
                    future_score,
                    2
                )

            })

        return {

            "profession":

                self.profession(
                    profession_id
                ),

            "current_score":

                current_score,

            "target_score":

                100.0,

            "steps":

                roadmap

        }

    # ------------------------------------------------------------

    def market_score(
        self,
        profession_id: str
    ) -> float:
        """
        Market demand estimate.

        Current implementation is based
        on connected vacancies.

        Can later include:
            • LinkedIn
            • Djinni
            • Work.ua
            • O*NET
            • ESCO trends
        """

        vacancies = self.professions.neighbour_vacancies(
            profession_id
        )

        return float(len(vacancies))

    # ------------------------------------------------------------

    def salary_forecast(
        self,
        profession_id: str
    ) -> float:
        """
        Average salary estimation.
        """

        vacancies = self.professions.neighbour_vacancies(
            profession_id
        )

        salaries = []

        for vacancy in vacancies:

            value = getattr(

                vacancy,

                "salary_max",

                0

            )

            if value:

                salaries.append(value)

        if not salaries:

            return 0.0

        return round(

            sum(salaries) /

            len(salaries),

            2

        )

    # ------------------------------------------------------------

    def profession_dashboard(
        self,
        profession_id: str,
        user_skill_ids: list[str]
    ) -> dict:
        """
        Complete dashboard
        for Human Workspace.
        """

        return {

            "profession":

                self.profession(
                    profession_id
                ),

            "score":

                self.readiness_score(

                    profession_id,

                    user_skill_ids

                ),

            "market":

                self.market_score(
                    profession_id
                ),

            "salary":

                self.salary_forecast(
                    profession_id
                ),

            "missing":

                self.missing_skills(

                    profession_id,

                    user_skill_ids

                ),

            "roadmap":

                self.learning_plan(

                    profession_id,

                    user_skill_ids

                )

        }

        # ------------------------------------------------------------
        # AI DECISION ENGINE
        # ------------------------------------------------------------

        def future_professions(
                self,
                profession_id: str,
                depth: int = 2
        ):
            """
            Predict possible future professions.

            Uses KnowledgeGraph neighbourhood.
            """

            graph = self.graph.subgraph(
                profession_id,
                depth
            )

            professions = []

            for node in graph["nodes"]:

                if isinstance(node, Profession):
                    professions.append(node)

            return professions

        # ------------------------------------------------------------

        def profession_report(
                self,
                profession_id: str,
                user_skill_ids: list[str]
        ) -> dict:
            """
            Complete profession report.
            """

            match = self.profession_match(
                profession_id,
                user_skill_ids
            )

            dashboard = self.profession_dashboard(
                profession_id,
                user_skill_ids
            )

            return {

                "profession":
                    dashboard["profession"],

                "match":

                    match,

                "market":

                    dashboard["market"],

                "salary":

                    dashboard["salary"],

                "roadmap":

                    dashboard["roadmap"],

                "future":

                    self.future_professions(
                        profession_id
                    )

            }

        # ------------------------------------------------------------

        def human_report(
                self,
                skill_ids: list[str]
        ) -> dict:
            """
            Complete report for Human Workspace.
            """

            best = self.best_profession(
                skill_ids
            )

            if best is None:
                return {

                    "success": False,

                    "message": "No profession found."

                }

            profession = best["profession"]

            return {

                "success": True,

                "best_profession":

                    profession,

                "score":

                    best["score"],

                "top20":

                    self.ranking(
                        skill_ids,
                        20
                    ),

                "career":

                    self.learning_plan(
                        profession.id,
                        skill_ids
                    ),

                "dashboard":

                    self.profession_dashboard(
                        profession.id,
                        skill_ids
                    )

            }

        # ------------------------------------------------------------

        def explain(
                self,
                profession_id: str,
                user_skill_ids: list[str]
        ) -> str:
            """
            Human readable explanation.
            """

            report = self.profession_match(
                profession_id,
                user_skill_ids
            )

            return (

                f"Current match: "

                f"{report['score']}%. "

                f"You already have "

                f"{report['matched']} "

                f"required skills. "

                f"{report['missing']} "

                f"skills should be learned "

                f"to reach full readiness."

            )

        # ------------------------------------------------------------

        def system_statistics(
                self
        ) -> dict:
            """
            Runtime statistics.
            """

            return {

                "professions":

                    self.professions.count(),

                "skills":

                    self.skills.count(),

                "graph":

                    self.graph.statistics()

            }

    # ============================================================
    # GLOBAL SINGLETON
    # ============================================================

    recommendation_engine = RecommendationEngine()