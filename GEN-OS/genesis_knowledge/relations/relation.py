"""
==========================================================
GENESIS HR®
Knowledge Relation
Универсальная связь графа знаний.
==========================================================
"""

from dataclasses import dataclass,field
from typing import Dict


@dataclass
class Relation:
    source:str
    target:str
    relation_type:str
    weight:int=100
    confidence:float=1.0
    source_provider:str="manual"
    enabled:bool=True
    metadata:Dict=field(default_factory=dict)