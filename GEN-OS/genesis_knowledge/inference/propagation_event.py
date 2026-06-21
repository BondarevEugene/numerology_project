"""
═══════════════════════════════════════════════════════════════
GENESIS HR®

Propagation Event
═══════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass


@dataclass

class PropagationEvent:

    source:str

    target:str

    relation:str

    value:float