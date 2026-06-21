"""
═══════════════════════════════════════════════════════════════
GENESIS HR®
Human Variable
═══════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass


@dataclass
class StateVariable:
    code: str
    title: str
    value: float = 50.0
    minimum: float = 0.0
    maximum: float = 100.0
