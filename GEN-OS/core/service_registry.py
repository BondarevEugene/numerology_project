"""
═══════════════════════════════════════════════════════════════════════════════

 GENESIS HR® // OMNIFACTORY EVO
 GEN-OS Platform
 MODULE
 -----------------------------------------------------------------------------
 Service Registry
 FILE
 -----------------------------------------------------------------------------
 service_registry.py
 BUILD
 -----------------------------------------------------------------------------
 0152
 DESCRIPTION
 -----------------------------------------------------------------------------

 ServiceRegistry является центральным контейнером сервисов
 платформы GEN-OS.
 Назначение:
    • регистрация сервисов
    • разрешение зависимостей
    • проверка готовности Runtime
    • единая точка доступа к сервисам

 Сервисы регистрируются по типу, а не по строковому имени.
 Пример:
     registry.register(
         PredictionService,
         prediction_service
     )
     prediction = registry.resolve(
         PredictionService
     )
═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

from typing import Any
import logging

LOGGER = logging.getLogger("GEN-OS.ServiceRegistry")


class ServiceRegistry:
    """
    Enterprise Dependency Container.
    """

    # ============================================================
    # LIFECYCLE
    # ============================================================

    def __init__(self):
        self._services: dict[type, Any] = {}

    # ============================================================
    # REGISTRATION
    # ============================================================

    def register(
        self,
        service_type: type,
        instance: Any
    ) -> None:
        """
        Register service instance.
        """
        LOGGER.info(
            "Register service: %s",
            service_type.__name__
        )

        self._services[service_type] = instance

    # ------------------------------------------------------------

    def unregister(
        self,
        service_type: type
    ) -> None:
        """
        Remove service.
        """

        self._services.pop(
            service_type,
            None
        )

    # ============================================================
    # RESOLVE
    # ============================================================

    def resolve(
        self,
        service_type: type
    ) -> Any:
        """
        Resolve service by type.
        """

        if service_type not in self._services:
            raise LookupError(
                f"Service "
                f"{service_type.__name__}"
                f" is not registered."
            )
        return self._services[service_type]

    # ------------------------------------------------------------

    def try_resolve(
        self,
        service_type: type
    ) -> Any | None:
        """
        Safe resolve.
        """
        return self._services.get(
            service_type
        )

    # ============================================================
    # INFORMATION
    # ============================================================

    def registered_types(
        self
    ) -> list[type]:
        """
        Returns registered service types.
        """
        return list(
            self._services.keys()
        )

    # ------------------------------------------------------------

    def registered_names(
        self
    ) -> list[str]:
        """
        Returns registered service names.
        """
        return [
            service.__name__
            for service
            in self._services
        ]

    # ------------------------------------------------------------

    def count(
        self
    ) -> int:
        """
        Number of services.
        """
        return len(
            self._services
        )

    # ============================================================
    # MAINTENANCE
    # ============================================================

    def clear(
        self
    ) -> None:
        """
        Remove every registered service.
        """
        self._services.clear()

    # ------------------------------------------------------------

    def contains(
        self,
        service_type: type
    ) -> bool:
        return service_type in self._services

    # ------------------------------------------------------------

    def information(
        self
    ) -> dict:
        """
        Registry information.
        """
        return {
            "services": self.count(),
            "registered": self.registered_names()

        }

    # ============================================================
    # MAGIC
    # ============================================================

    def __len__(self):
        return self.count()

    # ------------------------------------------------------------

    def __contains__(
        self,
        service_type: type
    ):
        return self.contains(
            service_type
        )

    # ------------------------------------------------------------

    def __repr__(
        self
    ):
        return (
            "<ServiceRegistry "
            f"services={self.count()}>"
        )


# ===============================================================
# GLOBAL REGISTRY
# ===============================================================

service_registry = ServiceRegistry()