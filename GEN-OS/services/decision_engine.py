"""
═══════════════════════════════════════════════════════════════════════════════
 GENESIS HR® // OMNIFACTORY EVO
 GEN-OS Platform
 MODULE
 -----------------------------------------------------------------------------
 Decision Engine
 FILE
 -----------------------------------------------------------------------------
 decision_engine.py
 BUILD
 -----------------------------------------------------------------------------
 0141
 DESCRIPTION
 -----------------------------------------------------------------------------
 Decision Engine является центральным модулем принятия решений GEN-OS.
 Он объединяет результаты анализа различных подсистем
 платформы и формирует единое интеллектуальное решение.
 Источники данных:
    • Knowledge Registry
    • Knowledge Graph
    • Prediction Engine
 В текущей версии реализованы:
    • Rule Engine
    • Priority Engine
    • Decision Builder
 Следующие версии будут содержать:
    • AI Reasoning
    • Scenario Planning
    • Monte-Carlo Simulation
    • Multi Goal Optimizer
 Decision Engine НЕ занимается:
    ✘ Import
    ✘ UI
    ✘ Database
    ✘ Graph Building
═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import logging

from dataclasses import dataclass
from dataclasses import field

from models.decision_result import DecisionResult
from models.prediction_result import PredictionResult

LOGGER = logging.getLogger("GEN-OS.Decision")


# ============================================================
# ACTION MODEL
# ============================================================

@dataclass(slots=True)
class DecisionAction:
    """
    Single executable action.
    """
    title: str
    category: str
    priority: int
    explanation: str = ""
    metadata: dict = field(
        default_factory=dict
    )


class DecisionEngine:
    """
    Enterprise Decision Engine.
    """

    # ============================================================
    # LIFECYCLE
    # ============================================================
    def __init__(self):
        self.registry = None
        self.graph = None
        self.prediction_engine = None

    # ------------------------------------------------------------

    def attach_registry(
            self,
            registry
    ):
        self.registry = registry

    # ------------------------------------------------------------

    def attach_graph(
            self,
            graph
    ):
        self.graph = graph

    # ------------------------------------------------------------
    def attach_prediction_engine(
            self,
            prediction_engine
    ):
        self.prediction_engine = prediction_engine

    # ============================================================
    # VALIDATION
    # ============================================================

    def validate(self):
        """
        Validates attached services.
        """
        if self.prediction_engine is None:
            raise RuntimeError(
                "Prediction Engine is not attached."
            )
        return True

    # ============================================================
    # PUBLIC API
    # ============================================================

    def decide(
            self,
            profile,
            profession=None
    ) -> DecisionResult:
        """
        Main Decision API.
        """
        self.validate()
        LOGGER.info(
            "Decision Engine started."
        )
        prediction = self.prediction_engine.predict(
            profile,
            profession
        )
        return self.build_decision(
            prediction
        )

    # ============================================================
    # DECISION BUILDER
    # ============================================================

    def build_decision(self, prediction: PredictionResult) -> DecisionResult:
        """
        Converts Prediction
        into Decision.
        """
        result = DecisionResult()
        result.confidence = prediction.confidence
        result.score = prediction.growth_score
        result.estimated_growth = prediction.growth_score
        result.estimated_risk = prediction.risk_score
        # Evaluate decision rules
        #
        self.evaluate_rules(
            prediction,
            result
        )
        return result

    # ============================================================
    # RULE ENGINE
    # ============================================================

    def evaluate_rules(
            self,
            prediction: PredictionResult,
            result: DecisionResult
    ) -> None:
        """
        Evaluate all registered decision rules.
        Rules are executed sequentially.
        """
        self.rule_high_growth(
            prediction,
            result
        )
        self.rule_high_risk(
            prediction,
            result
        )
        self.rule_learning_required(
            prediction,
            result
        )
        self.rule_confidence(
            prediction,
            result
        )
        # ============================================================
        # DECISION RULES
        # ============================================================

    def rule_high_growth(self, prediction: PredictionResult, result: DecisionResult) -> None:
        """
            High growth potential.
            """
        if prediction.growth_score >= 80:
            result.priority += 30
            result.metadata["growth"] = "HIGH"

    # ------------------------------------------------------------#
    def rule_high_risk(self, prediction: PredictionResult, result: DecisionResult) -> None:
        """
            High career risk.
            """
        if prediction.risk_score >= 60:
            result.priority += 15
            result.metadata["risk"] = "HIGH"

    # ------------------------------------------------------------

    def rule_learning_required(self, prediction: PredictionResult, result: DecisionResult) -> None:
        """
            Missing skills require learning.
            """
        if prediction.missing_skills:
            result.priority += len(
                prediction.missing_skills
            )
            result.recommended_skills.extend(
                prediction.missing_skills)

    # ------------------------------------------------------------ #

    def rule_confidence(self, prediction: PredictionResult, result: DecisionResult) -> None:
        """
            Confidence evaluation.
            """
        if prediction.confidence >= 0.80:
            result.metadata["confidence"] = "HIGH"
        elif prediction.confidence >= 0.50:
            result.metadata["confidence"] = "MEDIUM"
        else:
            result.metadata["confidence"] = "LOW"

    # ============================================================
    # DECISION BUILDER
    # ============================================================

    def build_decision(self, prediction: PredictionResult) -> DecisionResult:
        """
        Build DecisionResult from PredictionResult.
        """
        result = DecisionResult()
        #
        # Base metrics
        #
        result.confidence = prediction.confidence
        result.score = prediction.growth_score
        result.estimated_growth = prediction.growth_score
        result.estimated_risk = prediction.risk_score
        result.recommended_skills.extend(prediction.missing_skills)
        #
        # Evaluate all rules
        #

        self.evaluate_rules(
            prediction,
            result
        )
        #
        # Calculate final priority
        #
        result.priority = self.calculate_priority(result)

        result.metadata["actions"] = [
            action.__dict__
            for action
            in self.build_action_plan(prediction)
        ]
        #
        # Generate explanation
        #
        result.explanation = self.generate_explanation(
            prediction,
            result
        )
        return result

    # ============================================================
    # RULE ENGINE
    # ============================================================

    def evaluate_rules(
            self,
            prediction: PredictionResult,
            result: DecisionResult
    ) -> None:
        """
        Execute every decision rule.
        """

        self.rule_high_growth(
            prediction,
            result
        )

        self.rule_high_risk(
            prediction,
            result
        )

        self.rule_learning_required(
            prediction,
            result
        )

        self.rule_confidence(
            prediction,
            result
        )

        # ============================================================
        # DECISION RULES
        # ============================================================

    def rule_high_growth(
            self,
            prediction: PredictionResult,
            result: DecisionResult
    ) -> None:
        """
            High growth potential.
            """
        if prediction.growth_score >= 80:
            result.metadata["growth"] = "HIGH"

            result.priority += 30

    # ------------------------------------------------------------

    def rule_high_risk(
            self,
            prediction: PredictionResult,
            result: DecisionResult
    ) -> None:
        """
            High career risk.
            """
        if prediction.risk_score >= 60:
            result.metadata["risk"] = "HIGH"

            result.priority += 15

    # ------------------------------------------------------------

    def rule_learning_required(self, prediction: PredictionResult, result: DecisionResult) -> None:
        """
            Missing skills require learning.
            """
        if prediction.missing_skills:
            result.metadata["learning"] = True
            result.priority += len(
                prediction.missing_skills
            )

    # ------------------------------------------------------------

    def rule_confidence(self, prediction: PredictionResult, result: DecisionResult) -> None:
        """
            Confidence evaluation.
            """
        if prediction.confidence >= 0.80:
            result.metadata["confidence"] = "HIGH"
        elif prediction.confidence >= 0.50:
            result.metadata["confidence"] = "MEDIUM"
        else:
            result.metadata["confidence"] = "LOW"

    # ============================================================
    # PRIORITY ENGINE
    # ============================================================

    def calculate_priority(
            self,
            result: DecisionResult
    ) -> int:
        """
        Calculate final priority score.
        This score is later used for
        recommendation sorting and
        decision ranking.
        """
        priority = result.priority
        #
        # Growth factor
        #
        if result.estimated_growth >= 90:
            priority += 25
        elif result.estimated_growth >= 75:
            priority += 15
        #
        # Risk factor
        #
        if result.estimated_risk >= 75:
            priority += 20
        elif result.estimated_risk >= 50:
            priority += 10
        #
        # Confidence factor
        #
        if result.confidence >= 0.90:
            priority += 10
        elif result.confidence >= 0.75:
            priority += 5
        return priority

    # ============================================================
    # ACTION PLANNER
    # ============================================================

    # ============================================================
    # ACTION PLANNER
    # ============================================================

    def build_action_plan(self, prediction: PredictionResult) -> list[DecisionAction]:
        """
        Generate prioritized action plan.
        """
        actions = []
        #
        # Missing skills
        #
        for skill in prediction.missing_skills:
            actions.append(
                DecisionAction(
                    title=f"Study {skill}",
                    category="skill",
                    priority=100,
                    explanation=(
                        f"Acquire '{skill}' "
                        "to increase career opportunities."
                    )
                )
            )
        #
        # Sort
        #
        actions.sort(
            key=lambda action: action.priority,
            reverse=True
        )
        return actions

    # ============================================================
    # VERSION
    # ============================================================

    VERSION = "1.0.0"
    BUILD = "0141"
    ENGINE = "Decision Engine"
    # ============================================================
    # INFORMATION
    # ============================================================

    def information(self) -> dict:
        """
        Returns engine information.
        """
        return {
            "engine": self.ENGINE,
            "version": self.VERSION,
            "build": self.BUILD,
            "prediction_attached":
                self.prediction_engine is not None,
            "graph_attached":
                self.graph is not None,
            "registry_attached":
                self.registry is not None
        }

    # ============================================================
    # HEALTH CHECK
    # ============================================================

    def health(self) -> dict:
        """
        Returns current engine status.
        """
        return {

            "healthy":
                self.prediction_engine is not None,
            "ready":
                self.validate() is None,
            "information":
                self.information()

        }

    # ============================================================
    # DEBUG
    # ============================================================

    def __repr__(self):
        return (
            "<DecisionEngine "
            f"version={self.VERSION} "
            f"build={self.BUILD}>"
        )

    # ============================================================
    # GLOBAL ENGINE
    # ============================================================

    decision_engine = DecisionEngine()

