"""
══════════════════════════════════════════════════════════════

GENESIS HR®

Digital Human Twin

Subsystem:
Digital Twin Core

Description:
Главный агрегатор цифрового двойника человека.

══════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass, field

from .identity import IdentityProfile
from .cognition import CognitionProfile
from .competencies import CompetencyProfile
from .potential import PotentialProfile
from .prediction import PredictionProfile
from .timeline import TimelineProfile


@dataclass
class DigitalTwin:

    identity: IdentityProfile
    cognition: CognitionProfile
    competencies: CompetencyProfile
    potential: PotentialProfile
    prediction: PredictionProfile
    timeline: TimelineProfile
    version: str = "0.1"
    health: float = 1.0
    confidence: float = 0.0
    completeness: float = 0.0