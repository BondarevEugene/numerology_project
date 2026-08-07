"""
═══════════════════════════════════════════════════════════════════════════════

 GENESIS HR® // OMNIFACTORY EVO
 GEN-OS Platform
 MODULE
-----------------------------------------------------------------------------
 Import Service
 FILE
-----------------------------------------------------------------------------
 import_service.py
 BUILD
-----------------------------------------------------------------------------
 0035
 DESCRIPTION
-----------------------------------------------------------------------------

 Центральный сервис импорта платформы.
 ImportService НЕ занимается разбором файлов.

 Он:
    • регистрирует Import Providers
    • запускает импорт
    • уведомляет платформу о завершении
 Поддерживаемые источники:

    • CSV
    • Excel
    • JSON
    • ESCO
    • O*NET
    • REST API
    • AI Import

═══════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations
import logging
LOGGER = logging.getLogger("GEN-OS.Import")


class ImportService:
    """
    Central import orchestrator.
    """

    # ============================================================
    # LIFECYCLE
    # ============================================================

    def __init__(self):
        self.providers: dict = {}
        self.context = None
        self.registry = None
        self.event_bus = None

    # ============================================================
    # CONTEXT
    # ============================================================

    def attach_context(
        self,
        context
    ) -> None:
        """
        Attach PlatformContext.
        """
        self.context = context
        self.registry = context.registry
        self.event_bus = context.event_bus

    # ============================================================
    # PROVIDERS
    # ============================================================

    def register(
        self,
        name: str,
        provider
    ) -> None:
        """
        Register import provider.
        """

        LOGGER.info(
            "Import provider registered: %s",
            name
        )

        self.providers[name] = provider

    # ------------------------------------------------------------

    def exists(
        self,
        provider: str
    ) -> bool:

        return provider in self.providers

    # ------------------------------------------------------------

    def providers_list(
        self
    ) -> list[str]:

        return sorted(
            self.providers.keys()
        )

    # ============================================================
    # IMPORT
    # ============================================================

    def import_file(
        self,
        provider: str,
        filename: str
    ):
        """
        Execute import using selected provider.
        """
        if provider not in self.providers:
            raise ValueError(
                f"Provider '{provider}' is not registered."
            )
        LOGGER.info(
            "Import started: %s (%s)",
            filename,
            provider
        )
        result = self.providers[
            provider
        ].import_file(
            filename
        )

        LOGGER.info(
            "Import completed: %s",
            filename
        )
        #
        # Notify platform
        #
        if self.event_bus is not None:
            self.event_bus.emit(
                "import.completed",
                provider=provider,
                filename=filename,
                result=result
            )
        return result

    # ============================================================
    # INFORMATION
    # ============================================================

    def statistics(
        self
    ) -> dict:
        return {
            "providers": len(self.providers),
            "registered": self.providers_list()
        }

    # ------------------------------------------------------------

    def __len__(self):
        return len(self.providers)

    # ------------------------------------------------------------

    def __repr__(self):
        return (
            "<ImportService "
            f"providers={len(self.providers)}>"
        )


# ===============================================================
# GLOBAL INSTANCE
# ===============================================================

import_service = ImportService()
