"""
═══════════════════════════════════════════════════════════════════════════════

 GENESIS HR® // OMNIFACTORY EVO

 GEN-OS Platform

 MODULE
-----------------------------------------------------------------------------
 Kernel Module

 FILE
-----------------------------------------------------------------------------
 module.py

 BUILD
-----------------------------------------------------------------------------
 0158

 DESCRIPTION
-----------------------------------------------------------------------------

 Базовый класс любого модуля платформы GEN-OS.

 Каждый модуль (Knowledge, Human, Import, AI, Prediction,
 Decision, Career и т.д.) наследуется от KernelModule.

 KernelModule определяет единый жизненный цикл модулей.

 Responsibilities

    • Service Registration

    • Event Registration

    • Workspace Registration

    • Initialization

    • Startup

    • Shutdown

═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

import logging

LOGGER = logging.getLogger("GEN-OS.KernelModule")


class KernelModule(ABC):
    """
    Base platform module.
    """

    NAME = "Base Module"

    VERSION = "1.0.0"

    BUILD = "0158"

    DESCRIPTION = ""

    # ============================================================
    # REGISTRATION
    # ============================================================

    @abstractmethod
    def register_services(
        self,
        kernel
    ) -> None:
        """
        Register services.
        """
        ...

    # ------------------------------------------------------------

    @abstractmethod
    def register_events(
        self,
        kernel
    ) -> None:
        """
        Register EventBus listeners.
        """
        ...

    # ------------------------------------------------------------

    @abstractmethod
    def register_workspaces(
        self,
        kernel
    ) -> None:
        """
        Register workspaces.
        """
        ...

    # ============================================================
    # LIFECYCLE
    # ============================================================

    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize module.
        """
        ...

    # ------------------------------------------------------------

    def start(self) -> None:
        """
        Optional startup.
        """
        LOGGER.info(
            "%s started.",
            self.NAME
        )

    # ------------------------------------------------------------

    def stop(self) -> None:
        """
        Optional shutdown.
        """
        LOGGER.info(
            "%s stopped.",
            self.NAME
        )

    # ============================================================
    # HEALTH
    # ============================================================

    def health(self) -> dict:
        """
        Module health.
        """

        return {

            "name": self.NAME,

            "version": self.VERSION,

            "build": self.BUILD,

            "healthy": True

        }

    # ============================================================
    # INFORMATION
    # ============================================================

    def information(self) -> dict:

        return {

            "name": self.NAME,

            "version": self.VERSION,

            "build": self.BUILD,

            "description": self.DESCRIPTION

        }

    # ============================================================
    # MAGIC
    # ============================================================

    def __repr__(self):

        return (

            "<KernelModule "

            f"{self.NAME} "

            f"{self.VERSION}>"

        )
