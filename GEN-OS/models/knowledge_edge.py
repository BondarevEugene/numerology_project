"""
═══════════════════════════════════════════════════════════════════════
GENESIS®
Knowledge Edge
BUILD 0103
═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass


@dataclass
class KnowledgeEdge:
    source: str
    target: str
    relation: str
    weight: float = 1.0
    bidirectional: bool = False
