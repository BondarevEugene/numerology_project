"""
═══════════════════════════════════════════════════════════════════════
GEN-OS®
Genesys Operating System
Workspace Registry

BUILD-0016
Главный реестр рабочих областей платформы.
Любой новый модуль регистрируется только здесь.
После регистрации Workspace автоматически становится
доступным для Shell.

═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass


@dataclass
class Workspace:
    id: str
    title: str
    subtitle: str
    icon: str
    template: str
    javascript: str
    enabled: bool = True


WORKSPACES = {
    "human": Workspace(
        id="human",
        title="Digital Twin",
        subtitle="Human Intelligence Workspace",
        icon="◎",
        template="workspaces/human/human.html",
        javascript="human_workspace.js"
    ),
    "career": Workspace(
        id="career",
        title="Career Intelligence",
        subtitle="Professional Analytics",
        icon="◈",
        template="workspaces/career/career.html",
        javascript="career_workspace.js"
    ),
    "knowledge": Workspace(
        id="knowledge",
        title="Knowledge Explorer",
        subtitle="Knowledge Graph",
        icon="⬢",
        template="workspaces/knowledge/knowledge.html",
        javascript="knowledge_workspace.js"
    ),
    "import": Workspace(
        id="import",
        title="Knowledge Import",
        subtitle="Excel • ESCO • O*NET",
        icon="⬒",
        template="workspaces/import/import.html",
        javascript="import_workspace.js"
    ),
    "simulation": Workspace(
        id="simulation",
        title="Future Simulator",
        subtitle="Predictive Engine",
        icon="◉",
        template="workspaces/simulation/simulation.html",
        javascript="simulation_workspace.js"
    ),
    "ai": Workspace(
        id="ai",
        title="AI Advisor",
        subtitle="Genesis Neural Core",
        icon="✦",
        template="workspace/ai/ai.html",
        javascript="ai_workspace.js"
    ),
    "platform": Workspace(
        id="platform",
        title="Platform",
        subtitle="Configuration",
        icon="⚙",
        template="workspaces/platform/platform.html",
        javascript="platform_workspace.js"
    ),
    "dashboard": Workspace(
        id="dashboard",
        title="dashboard",
        subtitle="Configuration",
        icon="!",
        template="workspace/dashboard/dashboard.html",
        javascript="dashboard_workspace.js"
    )

}
