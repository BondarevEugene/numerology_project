"""
═══════════════════════════════════════════════════════════════
GENESIS HR®

Graph Node
═══════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass, field


@dataclass

class Node:

    id:str

    entity_type:str

    title:str

    metadata:dict=field(default_factory=dict)