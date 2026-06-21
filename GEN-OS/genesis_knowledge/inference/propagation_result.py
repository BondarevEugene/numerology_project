"""
═══════════════════════════════════════════════════════════════
GENESIS HR®

Propagation Result
═══════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass, field


@dataclass

class PropagationResult:

    updated_entities:list=field(default_factory=list)

    events:list=field(default_factory=list)

    score_changes:dict=field(default_factory=dict)