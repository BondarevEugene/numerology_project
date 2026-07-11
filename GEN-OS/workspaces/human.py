"""
═══════════════════════════════════════════════════════════════════════

GENESIS HR®
GEN-OS

FILE:workspaces/human.py

BUILD:0600

DESCRIPTION
Human Workspace.
Главное рабочее пространство платформы.
Отвечает исключительно за:

• описание Workspace
• подключение шаблона
• подготовку контекста
• публикацию команд
• публикацию навигации

Бизнес-логика НЕ находится здесь.
Все данные предоставляет HumanWorkspaceService.
═══════════════════════════════════════════════════════════════════════
"""

from kernel.workspace_base import Workspace

from services.human_service import human_service


class HumanWorkspace(Workspace):

    # ==========================================================
    # IDENTITY
    # ==========================================================

    id = "human"
    title = "Digital Twin"
    icon = "brain"

    description = (
        "Digital Human Intelligence Workspace"
    )
    order = 10
    enabled = True
    menu = True
    visible = True
    template_name = "workspaces/human/human.html"

    # ==========================================================
    # LIFECYCLE
    # ==========================================================

    def boot(self):
        super().boot()
        return self

    # ==========================================================
    # TEMPLATE
    # ==========================================================

    def template(self):
        return self.template_name

    # ==========================================================
    # NAVIGATION
    # ==========================================================

    def navigation(self):
        return [
            {
                "id": "overview",
                "title": "Overview"
            },
            {
                "id": "competencies",
                "title": "Competencies"
            },
            {
                "id": "career",
                "title": "Career"
            },
            {
                "id": "prediction",
                "title": "Prediction"
            },
            {
                "id": "roadmap",
                "title": "Roadmap"
            }
        ]

    # ==========================================================
    # COMMANDS
    # ==========================================================

    def commands(self):
        return [
            {
                "id": "refresh",
                "title": "Refresh"
            },
            {
                "id": "export",
                "title": "Export"
            },
            {
                "id": "report",
                "title": "Generate Report"
            }
        ]

    # ==========================================================
    # WIDGETS
    # ==========================================================

    def widgets(self):
        return [
            "current_profile",
            "career_score",
            "system_status",
            "top_competencies",
            "future_prediction",
            "recommended_professions",
            "risk_analysis",
            "development_plan",
            "recommendation_feed"
        ]

    # ==========================================================
    # CONTEXT
    # ==========================================================

    def build_context(self):
        workspace = human_service.workspace()
        return {
            "workspace": self,
            "title": self.title,
            "profile": workspace.profile,
            "dashboard": workspace.dashboard,
            "competencies": workspace.competencies,
            "professions": workspace.professions,
            "risks": workspace.risks,
            "roadmap": workspace.roadmap,
            "navigation": self.navigation(),
            "commands": self.commands(),
            "widgets": self.widgets()
        }

    # ==========================================================
    # STATISTICS
    # ==========================================================

    def statistics(self):
        statistics = human_service.statistics()
        statistics["workspace"] = self.id
        statistics["loaded"] = self.loaded
        return statistics

    # ==========================================================
    # HEALTH
    # ==========================================================

    def health(self):
        return {
            "workspace": self.id,
            "loaded": self.loaded,
            "service": human_service.health()
        }

    # ==========================================================
    # DEBUG
    # ==========================================================

    def __repr__(self):

        return (

            "<HumanWorkspace "

            f"loaded={self.loaded}>"

        )