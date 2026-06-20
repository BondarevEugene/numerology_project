"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
GENOS UI ENGINE
Visual Component Registry
Version : 1.0
═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass,field
from typing import List,Optional


@dataclass
class Component:
    id:str=""
    title:str=""
    icon:str=""
    css_class:str=""
    visible:bool=True


@dataclass
class Button(Component):
    action:str=""
    color:str="gold"


@dataclass
class Search(Component):
    placeholder:str="Search..."


@dataclass
class Badge(Component):
    value:str=""
    color:str="success"


@dataclass
class KPI(Component):
    value:str=""
    subtitle:str=""


@dataclass
class Card(Component):
    body:str=""


@dataclass
class Panel(Component):
    children:List[Component]=field(default_factory=list)


@dataclass
class Table(Component):
    columns:List[str]=field(default_factory=list)
    rows:list=field(default_factory=list)


@dataclass
class Workspace(Component):
    left:List[Component]=field(default_factory=list)
    center:List[Component]=field(default_factory=list)
    right:List[Component]=field(default_factory=list)