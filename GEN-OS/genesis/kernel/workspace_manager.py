"""
═══════════════════════════════════════════════════════════════════════════════
GENESIS HR®
GEN-OS Platform

FILE:workspace_manager.py

BUILD:0021

LAYER:Kernel

DESCRIPTION
Workspace Manager.
Регистрирует все рабочие области платформы.
Workspace — это полноценная рабочая среда
(аналог окна IDE).
Все окна системы открываются только отсюда.

═══════════════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Optional


@dataclass
class Workspace:
    id: str
    title: str
    icon: str
    route: str
    description: str = ""
    enabled: bool = True
    order: int = 0


class WorkspaceManager:
    def __init__(self):
        self._workspaces: Dict[str, Workspace] = {}

    # ==========================================================
    # REGISTER
    # ==========================================================

    def register(
            self,
            workspace: Workspace
    ):
        self._workspaces[workspace.id] = workspace

    # ==========================================================
    # GET
    # ==========================================================

    def get(
            self,
            workspace_id: str
    ) -> Optional[Workspace]:
        return self._workspaces.get(
            workspace_id
        )

    # ==========================================================
    # EXISTS
    # ==========================================================

    def exists(
            self,
            workspace_id: str
    ) -> bool:
        return workspace_id in self._workspaces

    # ==========================================================
    # ENABLE
    # ==========================================================

    def enable(
            self,
            workspace_id: str
    ):
        if self.exists(workspace_id):
            self._workspaces[workspace_id].enabled = True

    # ==========================================================
    # DISABLE
    # ==========================================================

    def disable(
            self,
            workspace_id: str
    ):
        if self.exists(workspace_id):
            self._workspaces[workspace_id].enabled = False

    # ==========================================================
    # LIST
    # ==========================================================

    def all(self):
        return sorted(
            self._workspaces.values(),
            key=lambda x: x.order
        )

    # ==========================================================
    # ENABLED
    # ==========================================================

    def enabled(self):
        return [
            w
            for w
            in self.all()
            if w.enabled
        ]

    # ==========================================================
    # DEFAULT
    # ==========================================================

    def register_default_workspaces(self):
        self.register(
            Workspace(
                id="knowledge",
                title="Knowledge Workspace",
                icon="🧠",
                route="/knowledge",
                order=1
            )
        )
        self.register(
            Workspace(
                id="career",
                title="Career Studio",
                icon="💼",
                route="/career",
                order=2
            )
        )
        self.register(
            Workspace(
                id="human",
                title="Human Workspace",
                icon="👤",
                route="/human",
                order=3
            )
        )
        self.register(
            Workspace(
                id="prediction",
                title="Prediction Lab",
                icon="📈",
                route="/prediction",
                order=4
            )
        )
        self.register(
            Workspace(
                id="development",
                title="Development Planner",
                icon="🚀",
                route="/development",
                order=5
            )
        )
        self.register(
            Workspace(
                id="graph",
                title="Graph Explorer",
                icon="🕸",
                route="/graph",
                order=6
            )
        )
        self.register(
            Workspace(
                id="import",
                title="Import Station",
                icon="📥",
                route="/import",
                order=7
            )
        )
        self.register(
            Workspace(
                id="settings",
                title="Platform Settings",
                icon="⚙",
                route="/settings",
                order=100
            )
        )

    # ==========================================================
    # COUNT
    # ==========================================================

    @property
    def count(self):
        return len(
            self._workspaces
        )

    # ==========================================================
    # HEALTH
    # ==========================================================

    def health(self):
        return {
            "registered": self.count,
            "enabled": len(
                self.enabled()
            )
        }

    # ==========================================================
    # REPORT
    # ==========================================================

    def report(self):
        rows = []
        for w in self.all():
            rows.append({
                "id": w.id,
                "title": w.title,
                "route": w.route,
                "enabled": w.enabled
            })
        return rows

    # ==========================================================
    # MAGIC
    # ==========================================================

    def __contains__(
            self,
            workspace
    ):
        return self.exists(
            workspace
        )

    def __len__(
            self
    ):
        return self.count

    def __repr__(self):
        return (
            f"<WorkspaceManager "
            f"workspaces={self.count}>"
        )
