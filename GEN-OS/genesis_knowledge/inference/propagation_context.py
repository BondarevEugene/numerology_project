"""
═══════════════════════════════════════════════════════════════
GENESIS HR®

Propagation Context

Описание текущего расчета.
═══════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass, field
from typing import Dict


@dataclass

class PropagationContext:

    entity_id:str

    entity_type:str

    delta:float=1.0

    metadata:Dict=field(default_factory=dict)