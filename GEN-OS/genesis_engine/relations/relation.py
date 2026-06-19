"""
═══════════════════════════════════════════════════════════════════════

GENESIS KNOWLEDGE ENGINE
MODULE    Relation
MODULE ID    GKH-REL-001
VERSION    1.0.0 Alpha
LAYER    Knowledge Graph
DESCRIPTION

Universal relation connecting two Genesis
Knowledge Entities.
Everything in Genesis is connected through
Relations.
Examples

Profession
    ├── requires ─────────► Competency
    ├── recommends ───────► Book
    ├── develops ─────────► Habit
    ├── improved_by ──────► Protocol
    ├── suitable_for ─────► Archetype
    └── related_to ───────► Profession

The Graph Engine operates ONLY with Relations.
═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass
from dataclasses import field

from datetime import datetime

from typing import Dict
from typing import Any


@dataclass(slots=True)
class Relation:

    # ==========================================================
    # IDENTIFICATION
    # ==========================================================

    uuid: str
    source_uuid: str
    target_uuid: str
    relation_type: str

    # ==========================================================
    # WEIGHT
    # ==========================================================

    weight: float = 1.0
    confidence: float = 1.0
    bidirectional: bool = False

    # ==========================================================
    # META
    # ==========================================================

    source: str = "manual"
    status: str = "active"
    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    # ==========================================================
    # SERIALIZATION
    # ==========================================================

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "source_uuid": self.source_uuid,
            "target_uuid": self.target_uuid,
            "relation_type": self.relation_type,
            "weight": self.weight,
            "confidence": self.confidence,
            "bidirectional": self.bidirectional,
            "source": self.source,
            "status": self.status,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }

    def __repr__(self):
        return (
            f"<Relation "
            f"{self.relation_type}: "
            f"{self.source_uuid} -> "
            f"{self.target_uuid}>"
        )