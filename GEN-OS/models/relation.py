"""
═══════════════════════════════════════════════════════════════════════

GENESIS®

Ontology Relation

BUILD 0104

═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Relation:

    id: str = field(default_factory=lambda: str(uuid4()))

    source: str = ""

    target: str = ""

    relation: str = ""

    weight: float = 1.0

    bidirectional: bool = False

    confidence: float = 1.0

    metadata: dict = field(default_factory=dict)