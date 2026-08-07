"""
═══════════════════════════════════════════════════════════════════════════════

GENESIS HR® // OMNIFACTORY EVO

GEN-OS Platform

MODULE:
Decision Domain Model

FILE:
decision_result.py

BUILD:
0140

DESCRIPTION
-----------------------------------------------------------------------------
DecisionResult представляет собой канонический объект,
содержащий итоговое решение интеллектуального ядра GEN-OS.

Decision Engine является центральной системой принятия решений.

Все сервисы платформы работают НЕ напрямую друг с другом,
а через DecisionResult.

Используется:

    • Recommendation Engine
    • Career Engine
    • Simulation Engine
    • AI Workspace
    • REST API
    • Human Workspace

DecisionResult является DTO и не содержит бизнес-логики.

═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class DecisionResult:
    """
    Canonical decision object.
    """

    #
    # General
    #

    confidence: float = 0.0

    score: float = 0.0

    priority: int = 0

    #
    # Recommendation
    #

    next_action: str = ""

    explanation: str = ""

    #
    # Skill Development
    #

    recommended_skills: list[str] = field(default_factory=list)

    recommended_competencies: list[str] = field(default_factory=list)

    recommended_courses: list[str] = field(default_factory=list)

    #
    # Career
    #

    target_profession: str = ""

    career_path: list[str] = field(default_factory=list)

    #
    # Simulation
    #

    estimated_growth: float = 0.0

    estimated_risk: float = 0.0

    #
    # Metadata
    #

    metadata: dict[str, Any] = field(default_factory=dict)

    # ---------------------------------------------------------------------

    def to_dict(self) -> dict:

        return {

            "confidence": self.confidence,

            "score": self.score,

            "priority": self.priority,

            "next_action": self.next_action,

            "explanation": self.explanation,

            "recommended_skills":
                self.recommended_skills,

            "recommended_competencies":
                self.recommended_competencies,

            "recommended_courses":
                self.recommended_courses,

            "target_profession":
                self.target_profession,

            "career_path":
                self.career_path,

            "estimated_growth":
                self.estimated_growth,

            "estimated_risk":
                self.estimated_risk,

            "metadata":
                self.metadata

        }

    # ---------------------------------------------------------------------

    @property
    def has_recommendations(self) -> bool:

        return (

            bool(self.recommended_skills)

            or

            bool(self.recommended_courses)

            or

            bool(self.career_path)

        )