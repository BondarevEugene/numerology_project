"""
═══════════════════════════════════════════════════════════════════════════════

 GENESIS HR® // OMNIFACTORY EVO

 GEN-OS Platform

 MODULE
-----------------------------------------------------------------------------
 Lifecycle Manager

 FILE
-----------------------------------------------------------------------------
 lifecycle.py

 BUILD
-----------------------------------------------------------------------------
 0154

 DESCRIPTION
-----------------------------------------------------------------------------

 Lifecycle Manager управляет жизненным циклом платформы.

 Responsibilities

    • Registration

    • Initialization

    • Startup

    • Shutdown

    • Health Check

 Lifecycle НЕ знает ничего
 о конкретных сервисах.

 Любой компонент платформы должен
 реализовать одинаковый интерфейс.

═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import logging

from typing import Protocol

LOGGER = logging.getLogger("GEN-OS.Lifecycle")


# ============================================================
# LIFECYCLE PROTOCOL
# ============================================================

class LifecycleComponent(Protocol):
    """
    Every platform component should implement
    this interface.
    """

    def initialize(self) -> None:
        ...

    def start(self) -> None:
        ...

    def stop(self) -> None:
        ...

    def health(self) -> dict:
        ...


# ============================================================
# LIFECYCLE MANAGER
# ============================================================

class LifecycleManager:

    """
    Platform lifecycle manager.
    """

    def __init__(self):

        self._components: list[LifecycleComponent] = []

    # ========================================================
    # REGISTRATION
    # ========================================================

    def register(
        self,
        component: LifecycleComponent
    ) -> None:

        self._components.append(component)

        LOGGER.info(

            "Registered component: %s",

            component.__class__.__name__

        )

    # --------------------------------------------------------

    def unregister(
        self,
        component: LifecycleComponent
    ) -> None:

        if component in self._components:

            self._components.remove(component)

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def initialize(self) -> None:

        LOGGER.info(

            "Initializing platform..."

        )

        for component in self._components:

            component.initialize()

    # ========================================================
    # STARTUP
    # ========================================================

    def start(self) -> None:

        LOGGER.info(

            "Starting platform..."

        )

        for component in self._components:

            component.start()

    # ========================================================
    # SHUTDOWN
    # ========================================================

    def stop(self) -> None:

        LOGGER.info(

            "Stopping platform..."

        )

        for component in reversed(

            self._components

        ):

            component.stop()

    # ========================================================
    # HEALTH
    # ========================================================

    def health(self) -> dict:

        report = {}

        for component in self._components:

            report[

                component.__class__.__name__

            ] = component.health()

        return report

    # ========================================================
    # INFORMATION
    # ========================================================

    def information(self) -> dict:

        return {

            "components":

                len(self._components),

            "registered": [

                component.__class__.__name__

                for component

                in self._components

            ]

        }

    # ========================================================
    # MAGIC
    # ========================================================

    def __len__(self):

        return len(self._components)

    def __repr__(self):

        return (

            "<LifecycleManager "

            f"components={len(self)}>"

        )


# ============================================================
# GLOBAL INSTANCE
# ============================================================

lifecycle = LifecycleManager()