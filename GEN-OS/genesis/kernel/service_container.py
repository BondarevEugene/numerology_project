"""
═══════════════════════════════════════════════════════════════════════════════
GENESIS HR®
GEN-OS Platform

FILE:service_container.py
BUILD:0021
LAYER:Kernel

DESCRIPTION
Dependency Injection Container.
Все сервисы платформы регистрируются здесь.
Никакой модуль не должен самостоятельно создавать
KnowledgeService()
CareerEngine()
GraphEngine()

Получение только через Container.
Пример

container.register(
    "knowledge",
    KnowledgeService()
)
knowledge = container.get("knowledge")
═══════════════════════════════════════════════════════════════════════════════
"""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional


class ServiceContainer:
    """
    Центральный контейнер сервисов GENESIS.
    """
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._metadata: Dict[str, Dict] = {}
    # ==========================================================
    # REGISTER
    # ==========================================================

    def register(
        self,
        name: str,
        service: Any,
        version: str = "1.0",
        enabled: bool = True
    ) -> None:
        self._services[name] = service
        self._metadata[name] = {
            "version": version,
            "enabled": enabled,
            "class": service.__class__.__name__
        }

    # ==========================================================
    # GET
    # ==========================================================

    def get(
        self,
        name: str
    ) -> Optional[Any]:
        return self._services.get(
            name
        )

    # ==========================================================
    # REMOVE
    # ==========================================================

    def unregister(
        self,
        name: str
    ) -> bool:
        if name not in self._services:
            return False
        del self._services[name]
        del self._metadata[name]
        return True

    # ==========================================================
    # EXISTS
    # ==========================================================

    def exists(
        self,
        name: str
    ) -> bool:
        return name in self._services

    # ==========================================================
    # ENABLE
    # ==========================================================

    def enable(
        self,
        name: str
    ):
        if name in self._metadata:
            self._metadata[name]["enabled"] = True

    # ==========================================================
    # DISABLE
    # ==========================================================

    def disable(
        self,
        name: str
    ):
        if name in self._metadata:
            self._metadata[name]["enabled"] = False

    # ==========================================================
    # ENABLED
    # ==========================================================

    def enabled_services(self) -> List[str]:
        return [
            name
            for name, meta
            in self._metadata.items()
            if meta["enabled"]
        ]

    # ==========================================================
    # ALL
    # ==========================================================

    def services(self) -> List[str]:
        return sorted(
            self._services.keys()
        )

    # ==========================================================
    # METADATA
    # ==========================================================

    def metadata(
        self,
        name: str
    ) -> Dict:
        return self._metadata.get(
            name,
            {}
        )

    # ==========================================================
    # CLEAR
    # ==========================================================

    def clear(self):
        self._services.clear()
        self._metadata.clear()

    # ==========================================================
    # COUNT
    # ==========================================================

    @property
    def count(self):
        return len(
            self._services
        )

    # ==========================================================
    # HEALTH
    # ==========================================================

    def health(self):
        return {
            "registered": self.count,
            "enabled": len(
                self.enabled_services()
            ),
            "services": self.services()
        }

    # ==========================================================
    # DUMP
    # ==========================================================

    def dump(self):
        rows = []
        for name in self.services():
            meta = self.metadata(
                name
            )
            rows.append({
                "name": name,
                "class": meta.get("class"),
                "version": meta.get("version"),
                "enabled": meta.get("enabled")
            })
        return rows

    # ==========================================================
    # MAGIC
    # ==========================================================

    def __contains__(
        self,
        name
    ):
        return self.exists(
            name
        )

    def __getitem__(
        self,
        name
    ):
        return self.get(
            name
        )

    def __len__(
        self
    ):
        return self.count

    def __repr__(self):
        return (
            f"<ServiceContainer "
            f"services={self.count}>"
        )
