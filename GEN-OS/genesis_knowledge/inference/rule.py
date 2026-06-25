"""
==========================================================
GENESIS HR®
Inference Rule
Version:1.0
==========================================================
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class Rule:

    id:str
    title:str
    description:str
    condition:Dict
    action:Dict
    priority:int=100
    confidence:float=1.0
    enabled:bool=True
