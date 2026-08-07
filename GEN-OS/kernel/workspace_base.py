"""
═══════════════════════════════════════════════════════════════════════
GENESIS PLATFORM
Workspace Base Class
BUILD 0500
Все рабочие пространства платформы наследуются
от этого класса.

═══════════════════════════════════════════════════════════════════════
"""

from abc import ABC


class Workspace(ABC):

    """
    Базовый класс рабочего пространства.
    HumanWorkspace
    AIWorkspace
    KnowledgeWorkspace
    ImportWorkspace
    ...
    наследуются отсюда.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    id = ""
    title = ""
    icon = "circle"
    description = ""
    order = 0
    enabled = True

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    # ---------------------------------------------------------
    # Template
    # ---------------------------------------------------------

    template_name = None

    def template(self):
        if self.template_name:
            return self.template_name

        return f"workspaces/{self.id}_workspace.html"
    menu = True
    visible = True

    def build_context(self):
        """
        Основной контекст Workspace.
        Переопределяется в наследниках.
        """
        return self.context()
    # ---------------------------------------------------------

    def __init__(self):
        self.loaded = False

    # ---------------------------------------------------------

    def boot(self):
        """
        Вызывается один раз
        при старте платформы.
        """
        self.loaded = True
    # ---------------------------------------------------------

    def context(self):
        """
        Контекст,
        который попадет в Jinja.
        """
        return {}

    # ---------------------------------------------------------

    def statistics(self):
        return {
            "id": self.id,
            "title": self.title,
            "loaded": self.loaded
        }

    # ---------------------------------------------------------

    def __repr__(self):
        return (
            f"<Workspace "
            f"{self.id}>"
        )
