"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®

GEN-OS Runtime

FILE:
workspace_runtime.py

BUILD:
0044

AUTHOR
OpenAI + Yevhenii Bondariev

DESCRIPTION
-----------

Главный Runtime платформы.

Является точкой соединения между Kernel,
Workspace и бизнес-сервисами.

Не содержит Flask.
Не содержит SQLAlchemy.
Не содержит HTML.

Назначение:

• запуск Workspace
• регистрация сервисов
• подготовка данных
• публикация событий
• предоставление Context для GUI

═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass
from typing import Dict
from typing import Any

from services.workspace_service import workspace_service
from services.human_service import HumanWorkspaceService
from services.import_service import ImportService
from services.knowledge_service import KnowledgeService
from services.search_service import SearchService


@dataclass
class WorkspaceContext:

    workspace: Any

    services: Dict[str, Any]

    data: Dict[str, Any]


class WorkspaceRuntime:

    def __init__(self):

        self.services = {}

        self.register_defaults()

    def register_defaults(self):

        self.register(
            "human",
            HumanWorkspaceService()
        )

        self.register(
            "knowledge",
            KnowledgeService()
        )

        self.register(
            "import",
            ImportService()
        )

        self.register(
            "search",
            SearchService()
        )

    def register(
            self,
            name,
            service
    ):

        self.services[name] = service

    def service(
            self,
            name
    ):

        return self.services.get(name)

    def start(
            self,
            workspace_id
    ):

        workspace = workspace_service.open(
            workspace_id
        )

        if workspace is None:

            return None

        context = WorkspaceContext(

            workspace=workspace,

            services=self.services,

            data={}
        )

        self.prepare(context)

        return context

    def prepare(
            self,
            context
    ):

        human = self.service(
            "human"
        )

        if human:

            context.data[
                "dashboard"
            ] = human.load_dashboard()

            context.data[
                "profile"
            ] = human.load_profile()

            context.data[
                "competencies"
            ] = human.load_top_competencies()

            context.data[
                "professions"
            ] = human.load_recommended_professions()

            context.data[
                "risks"
            ] = human.load_risks()

            context.data[
                "roadmap"
            ] = human.load_roadmap()

        return context


runtime = WorkspaceRuntime()