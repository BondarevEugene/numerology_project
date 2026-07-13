"""
═══════════════════════════════════════════════════════════════════════════════

GENESIS HR® // OMNIFACTORY EVO

GEN-OS Platform

MODULE:
Prediction Engine

FILE:
prediction_service.py

BUILD:
0133

DESCRIPTION
-----------------------------------------------------------------------------

Prediction Engine является первым уровнем интеллектуального анализа
GEN-OS.

Он НЕ занимается:

    • импортом данных
    • загрузкой файлов
    • построением графов
    • поиском по Registry

Prediction Engine получает уже подготовленные объекты платформы
и выполняет логический анализ.

В текущей версии реализованы:

    • Анализ профиля
    • Анализ навыков
    • Поиск Skill Gap
    • Расчет Growth Score
    • Расчет Risk Score
    • Формирование PredictionResult

Следующие версии будут использовать:

    • Knowledge Graph
    • Semantic Reasoning
    • Career Path Search
    • AI Explanation Engine
    • Simulation Engine

═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import logging

from models.prediction_result import PredictionResult

LOGGER = logging.getLogger("GEN-OS.Prediction")


class PredictionService:
    """
    Enterprise Prediction Engine.

    Build 0133
    """

    # ============================================================
    # LIFECYCLE
    # ============================================================

    def __init__(self):

        self.registry = None

        self.graph = None

    # ------------------------------------------------------------

    def attach_registry(self, registry):

        """
        Connect Knowledge Registry.
        """

        self.registry = registry

    # ------------------------------------------------------------

    def attach_graph(self, graph):

        """
        Connect Knowledge Graph.
        """

        self.graph = graph

    # ============================================================
    # PROFILE ANALYSIS
    # ============================================================

    def analyse_profile(
        self,
        profile
    ) -> dict:

        """
        Extract normalized profile.

        Пока это заглушка.

        В BUILD 0135 здесь будет работать
        Human Graph Analyzer.
        """

        return {

            "skills":

                getattr(
                    profile,
                    "skills",
                    []
                ),

            "competencies":

                getattr(
                    profile,
                    "competencies",
                    []
                ),

            "knowledge":

                getattr(
                    profile,
                    "knowledge",
                    []
                )

        }


    # ============================================================
    # SKILL GAP
    # ============================================================

    def find_skill_gaps(

        self,

        current_skills,

        required_skills

    ) -> list[str]:

        """
        Returns missing skills.
        """

        current = {

            skill.lower()

            for skill

            in current_skills

        }

        missing = []

        for skill in required_skills:

            if skill.lower() not in current:

                missing.append(skill)

        return missing

    # ============================================================
    # GROWTH SCORE
    # ============================================================

    def calculate_growth_score(
        self,
        profile_analysis: dict
    ) -> float:
        """
        Calculates growth potential.

        В Build 0133 используется простая эвристика.

        В следующих версиях расчет будет основан
        на семантическом графе знаний.
        """

        score = 0.0

        score += len(
            profile_analysis.get(
                "skills",
                []
            )
        ) * 4

        score += len(
            profile_analysis.get(
                "competencies",
                []
            )
        ) * 6

        score += len(
            profile_analysis.get(
                "knowledge",
                []
            )
        ) * 2

        return min(score, 100.0)

    # ============================================================
    # RISK SCORE
    # ============================================================

    def calculate_risk_score(
        self,
        missing_skills: list[str]
    ) -> float:
        """
        Calculates career risk.

        Чем больше отсутствующих навыков —
        тем выше риск.
        """

        score = len(
            missing_skills
        ) * 7.5

        return min(score, 100.0)

    # ============================================================
    # CONFIDENCE
    # ============================================================

    def calculate_confidence(
        self,
        profile_analysis: dict
    ) -> float:
        """
        Calculates confidence level
        of current prediction.

        Пока используется полнота профиля.

        Позже будет учитывать
        качество графа знаний,
        источники данных
        и статистическую достоверность.
        """

        total = (

            len(profile_analysis.get("skills", []))

            +

            len(profile_analysis.get("competencies", []))

            +

            len(profile_analysis.get("knowledge", []))

        )

        confidence = total / 25.0

        return min(confidence, 1.0)

    # ============================================================
    # PROFESSION REQUIREMENTS
    # ============================================================

    def required_skills(
        self,
        profession
    ) -> list[str]:
        """
        Returns required skills
        for profession.

        BUILD 0133

        Пока используется metadata.

        Позже будет использовать
        Knowledge Graph.
        """

        return getattr(
            profession,
            "required_skills",
            []
        )

    # ============================================================
    # PREDICTION
    # ============================================================

    def predict(
        self,
        profile,
        profession=None
    ) -> PredictionResult:
        """
        Performs complete prediction analysis.

        This is the main public entry point of
        Prediction Engine.

        Parameters
        ----------
        profile
            Human profile.

        profession
            Optional target profession.

        Returns
        -------
        PredictionResult
        """

        LOGGER.info(
            "Prediction Engine started."
        )

        #
        # -----------------------------------------
        # Profile Analysis
        # -----------------------------------------
        #

        analysis = self.analyse_profile(
            profile
        )

        #
        # -----------------------------------------
        # Required Skills
        # -----------------------------------------
        #

        required = []

        if profession is not None:

            required = self.required_skills(
                profession
            )

        #
        # -----------------------------------------
        # Missing Skills
        # -----------------------------------------
        #

        missing_skills = self.find_skill_gaps(

            analysis.get(
                "skills",
                []
            ),

            required

        )

        #
        # -----------------------------------------
        # Scores
        # -----------------------------------------
        #

        growth = self.calculate_growth_score(
            analysis
        )

        risk = self.calculate_risk_score(
            missing_skills
        )

        confidence = self.calculate_confidence(
            analysis
        )

        success = max(
            0.0,
            growth - risk
        )

        #
        # -----------------------------------------
        # Prediction Result
        # -----------------------------------------
        #

        result = PredictionResult(

            success_probability=success,

            growth_score=growth,

            risk_score=risk,

            confidence=confidence,

            existing_skills=analysis.get(
                "skills",
                []
            ),

            competencies=analysis.get(
                "competencies",
                []
            ),

            missing_skills=missing_skills

        )

        #
        # -----------------------------------------
        # Explanation
        # -----------------------------------------
        #

        result.explanation = self.generate_explanation(
            result
        )

        LOGGER.info(
            "Prediction completed."
        )

        return result

    # ============================================================
    # EXPLANATION
    # ============================================================

    def generate_explanation(
        self,
        result: PredictionResult
    ) -> str:
        """
        Generates human-readable explanation.

        Later this block will be replaced by
        AI Reasoning Engine.
        """

        lines = []

        lines.append(
            f"Growth score: {result.growth_score:.1f}"
        )

        lines.append(
            f"Risk score: {result.risk_score:.1f}"
        )

        lines.append(
            f"Confidence: {result.confidence:.2f}"
        )

        if result.missing_skills:

            lines.append("Missing skills:")

            for skill in result.missing_skills:

                lines.append(
                    f" • {skill}"
                )

        else:

            lines.append(
                "Required skills are present."
            )

        return "\n".join(lines)


