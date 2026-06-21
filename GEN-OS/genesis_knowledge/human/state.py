"""
═══════════════════════════════════════════════════════════════
GENESIS HR®

Human State
═══════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass, field


@dataclass
class HumanState:
    variables: dict = field(default_factory=dict)
    score: float = 0.0
