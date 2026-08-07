class KernelComponent:

    def initialize(self):
        ...

    def start(self):
        ...

    def stop(self):
        ...

    def health(self):"""
═══════════════════════════════════════════════════════════════════════════════

 GENESIS HR® // OMNIFACTORY EVO

 GEN-OS Platform

 MODULE
-----------------------------------------------------------------------------
 Kernel Component

 FILE
-----------------------------------------------------------------------------
 component.py

 BUILD
-----------------------------------------------------------------------------
 0159

 DESCRIPTION
-----------------------------------------------------------------------------

 Базовый класс любого компонента платформы.

 Компонент является частью Module.

 Например

 Knowledge Module

      ├── Registry Component

      ├── Graph Component

      ├── Import Component

 Decision Module

      ├── Prediction Component

      ├── Decision Component

      ├── Recommendation Component

═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

from abc import ABC

import logging

LOGGER = logging.getLogger(
    "GEN-OS.Component"
)


class KernelComponent(ABC):

    """
    Base platform component.
    """

    NAME = "Component"

    VERSION = "1.0.0"

    BUILD = "0159"

    DESCRIPTION = ""

    def __init__(self):

        self.kernel = None

        self.context = None

    # ============================================================
    # ATTACH
    # ============================================================

    def attach_kernel(
        self,
        kernel
    ):

        self.kernel = kernel

    # ------------------------------------------------------------

    def attach_context(
        self,
        context
    ):

        self.context = context

    # ============================================================
    # LIFECYCLE
    # ============================================================

    def initialize(self):

        LOGGER.info(

            "%s initialized.",

            self.NAME

        )

    # ------------------------------------------------------------

    def start(self):

        LOGGER.info(

            "%s started.",

            self.NAME

        )

    # ------------------------------------------------------------

    def stop(self):

        LOGGER.info(

            "%s stopped.",

            self.NAME

        )

    # ============================================================
    # HEALTH
    # ============================================================

    def health(self):

        return {

            "healthy": True,

            "component": self.NAME,

            "version": self.VERSION

        }

    # ============================================================
    # INFORMATION
    # ============================================================

    def information(self):

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

            "<KernelComponent "

            f"{self.NAME}>"

        )
        return {}
