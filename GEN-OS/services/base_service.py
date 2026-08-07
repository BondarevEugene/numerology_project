"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██████╗ ███████╗███╗   ██╗      ██████╗ ███████╗                           ║
║  ██╔════╝ ██╔════╝████╗  ██║     ██╔═══██╗██╔════╝                           ║
║  ██║  ███╗█████╗  ██╔██╗ ██║     ██║   ██║███████╗                           ║
║  ██║   ██║██╔══╝  ██║╚██╗██║     ██║   ██║╚════██║                           ║
║  ╚██████╔╝███████╗██║ ╚████║     ╚██████╔╝███████║                           ║
║   ╚═════╝ ╚══════╝╚═╝  ╚═══╝      ╚═════╝ ╚══════╝                           ║
║                                                                              ║
║──────────────────────────────────────────────────────────────────────────────║
║ MODULE      : Base Service                                                   ║
║ FILE        : services/base_service.py                                       ║
║ LAYER       : Business Logic                                                 ║
║ PURPOSE     : Common service contract for all GEN-OS modules                 ║
║ BUILD       : 0400                                                           ║
║ STATUS      : CORE                                                           ║
║                                                                              ║
║ DESCRIPTION                                                                  ║
║ -----------                                                                  ║
║ Defines a unified API for every business service in GEN-OS.                  ║
║ All domain services should inherit from BaseService and override              ║
║ only the methods they need.                                                  ║
║                                                                              ║
║ IMPLEMENTATIONS                                                              ║
║ ---------------                                                              ║
║ • HumanWorkspaceService                                                      ║
║ • KnowledgeService                                                           ║
║ • GraphService                                                               ║
║ • CareerService                                                              ║
║ • AIService                                                                  ║
║ • SimulationService                                                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

from abc import ABC
from typing import Any


class BaseService(ABC):
    """
    Base contract for every GEN-OS service.
    """

    def __init__(self):
        self.name = self.__class__.__name__
        self.version = "4.0"
        self.loaded = False

    # ==========================================================
    # LIFECYCLE
    # ==========================================================

    def boot(self) -> None:
        """
        Initialize service.
        """
        self.loaded = True

    def shutdown(self) -> None:
        """
        Shutdown service.
        """
        self.loaded = False

    def ready(self) -> bool:
        """
        Returns True when service is initialized.
        """
        return self.loaded

    # ==========================================================
    # WORKSPACE
    # ==========================================================

    def workspace(self) -> dict:
        """
        Complete workspace payload.
        """
        return {}

    def dashboard(self):
        """
        Dashboard cards.
        """
        return []

    def summary(self):
        """
        Summary information.
        """
        return {}

    def statistics(self):
        """
        Statistical information.
        """
        return {}

    # ==========================================================
    # DATA ACCESS
    # ==========================================================

    def all(self):
        return []

    def get(self, object_id: str):
        return None

    def search(self, query: str):
        return []

    # ==========================================================
    # CRUD
    # ==========================================================

    def create(self, data: Any):
        raise NotImplementedError

    def update(self, object_id: str, data: Any):
        raise NotImplementedError

    def delete(self, object_id: str):
        raise NotImplementedError

    # ==========================================================
    # EXPORT
    # ==========================================================

    def export(self):
        return self.workspace()

    # ==========================================================
    # HEALTH
    # ==========================================================

    def health(self):
        return {
            "service": self.name,
            "version": self.version,
            "ready": self.ready()
        }

    # ==========================================================
    # INFO
    # ==========================================================

    def info(self):
        return {
            "service": self.name,
            "version": self.version,
            "loaded": self.loaded
        }

    # ==========================================================
    # DEBUG
    # ==========================================================

    def __repr__(self):

        return (
            f"<{self.name} "
            f"version={self.version} "
            f"loaded={self.loaded}>"
        )
