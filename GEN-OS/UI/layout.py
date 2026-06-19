"""
==========================================================
GENESIS HR®

GENOS UI Layout Engine
Version:
0.1
Description:
Главный реестр рабочих областей платформы.
Все окна системы подключаются здесь.

==========================================================
"""

from dataclasses import dataclass


@dataclass
class WorkspaceModule:

    id: str
    title: str
    icon: str
    route: str
    component: str
    order: int = 0
    enabled: bool = True


WORKSPACE = [
    WorkspaceModule(
        id="career",
        title="Career Studio",
        icon="💼",
        route="/admin/career-center",
        component="career",
        order=1
    ),

    WorkspaceModule(
        id="import",
        title="Import Station",
        icon="📥",
        route="/admin/import-center",
        component="import",
        order=2

    ),

    WorkspaceModule(
        id="knowledge",
        title="Knowledge Registry",
        icon="🧠",
        route="/admin/knowledge",
        component="knowledge",
        order=3
    ),

    WorkspaceModule(
        id="prediction",
        title="Prediction Lab",
        icon="📈",
        route="/admin/prediction",
        component="prediction",
        order=4
    ),

    WorkspaceModule(
        id="development",
        title="Development",
        icon="🚀",
        route="/admin/development",
        component="development",
        order=5
    ),

    WorkspaceModule(

        id="graph",
        title="Graph",
        icon="🕸",
        route="/admin/nexus-hub",
        component="graph",
        order=6
    )
]