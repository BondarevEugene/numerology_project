"""
═══════════════════════════════════════════════════════════════════════════════
GENESIS HR®
GEN-OS Platform
FILE: module_manager.py
BUILD:0021
LAYER:Kernel
DESCRIPTION
Module Registry.
Все подсистемы платформы регистрируются здесь.
Kernel ничего не знает о внутренних деталях модулей.
Он знает только:
id
title
version
enabled
dependencies

═══════════════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional


@dataclass
class Module:
    id: str
    title: str
    version: str
    description: str = ""
    enabled: bool = True
    dependencies: List[str] = None
    created: datetime = datetime.utcnow()


class ModuleManager:
    """
    Реестр всех модулей платформы.
    """

    def __init__(self):
        self._modules: Dict[str, Module] = {}

    # ==========================================================
    # REGISTER
    # ==========================================================

    def register(
            self,
            module: Module
    ):
        self._modules[module.id] = module

    # ==========================================================
    # GET
    # ==========================================================

    def get(
            self,
            module_id: str
    ) -> Optional[Module]:
        return self._modules.get(
            module_id
        )

    # ==========================================================
    # EXISTS
    # ==========================================================

    def exists(
            self,
            module_id: str
    ) -> bool:
        return module_id in self._modules

    # ==========================================================
    # REMOVE
    # ==========================================================

    def unregister(
            self,
            module_id: str
    ):
        if module_id in self._modules:
            del self._modules[module_id]

    # ==========================================================
    # ENABLE
    # ==========================================================

    def enable(
            self,
            module_id: str
    ):
        if self.exists(module_id):
            self._modules[module_id].enabled = True

    # ==========================================================
    # DISABLE
    # ==========================================================

    def disable(
            self,
            module_id: str
    ):
        if self.exists(module_id):
            self._modules[module_id].enabled = False

    # ==========================================================
    # LIST
    # ==========================================================

    def modules(self):
        return sorted(
            self._modules.values(),
            key=lambda x: x.title

        )

    # ==========================================================
    # ENABLED
    # ==========================================================

    def enabled(self):
        return [
            module
            for module
            in self._modules.values()
            if module.enabled
        ]

    # ==========================================================
    # COUNT
    # ==========================================================

    @property
    def count(self):
        return len(
            self._modules
        )

    # ==========================================================
    # BOOTSTRAP
    # ==========================================================

    def register_default_modules(self):
        self.register(
            Module(
                id="knowledge",
                title="Knowledge Registry",
                version="1.0"
            )
        )
        self.register(
            Module(
                id="career",
                title="Career Studio",
                version="1.0"
            )
        )
        self.register(
            Module(
                id="prediction",
                title="Prediction Lab",
                version="1.0"
            )
        )
        self.register(
            Module(
                id="graph",
                title="Graph Explorer",
                version="1.0"
            )
        )
        self.register(
            Module(
                id="recommendation",
                title="Recommendation Engine",
                version="1.0"
            )
        )
        self.register(
            Module(
                id="development",
                title="Development Planner",
                version="1.0"
            )
        )
        self.register(
            Module(
                id="import",
                title="Import Station",
                version="1.0"
            )
        )
        self.register(
            Module(
                id="telemetry",
                title="Telemetry",
                version="1.0"
            )
        )
        self.register(
            Module(
                id="ai",
                title="AI Core",
                version="1.0"
            )
        )

    # ==========================================================
    # HEALTH
    # ==========================================================

    def health(self):
        return {
            "modules":
                self.count,
            "enabled":
                len(
                    self.enabled()
                )
        }

    # ==========================================================
    # REPORT
    # ==========================================================

    def report(self):
        result = []
        for module in self.modules():
            result.append({
                "id": module.id,
                "title": module.title,
                "version": module.version,
                "enabled": module.enabled
            })
        return result

    # ==========================================================
    # MAGIC
    # ==========================================================

    def __contains__(
            self,
            item
    ):
        return self.exists(
            item
        )

    def __len__(
            self
    ):
        return self.count

    def __repr__(self):
        return (
            f"<ModuleManager "
            f"modules={self.count}>"
        )
