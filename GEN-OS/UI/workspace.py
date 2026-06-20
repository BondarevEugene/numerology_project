"""
══════════════════════════════════════════════════════════════════════
GENESIS HR®
GENOS Workspace Engine
Subsystem:
GENOS UI
Build:
0002
Description:
Базовая модель любой рабочей области платформы.
Любой экран системы описывается данным объектом.

══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class WorkspaceWidget:
    id: str
    title: str
    component: str
    width: int = 12
    height: str = "auto"
    enabled: bool = True


@dataclass
class Workspace:
    id: str
    title: str
    subtitle: str
    icon: str
    route: str
    widgets: List[WorkspaceWidget] = field(default_factory=list)

    toolbar: bool = True
    sidebar: bool = True
    statusbar: bool = True
    inspector: bool = True
    telemetry: bool = True
    search: bool = True
    version: str = "G1"
