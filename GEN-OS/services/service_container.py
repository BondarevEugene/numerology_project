"""
═══════════════════════════════════════════════════════════════════════════════════════
 ██████╗ ███████╗███╗   ██╗███████╗███████╗██╗███████╗
██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔════╝██║██╔════╝
██║  ███╗█████╗  ██╔██╗ ██║█████╗  ███████╗██║███████╗
██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ╚════██║██║╚════██║
╚██████╔╝███████╗██║ ╚████║███████╗███████║██║███████║
 ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝╚══════╝

 Human Evolution Operating System
═══════════════════════════════════════════════════════════════════════════════════════

FILE    service_container.py

MODULE    Runtime Dependency Container

BUILD    0200

DESCRIPTION
    Central registry for runtime services.
    The Kernel never creates engines directly.
    Everything is resolved through the container.

═══════════════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations
from typing import Any


class ServiceContainer:

    def __init__(self):
        self._services = {}

    # ===================================================================
    def register(self, name: str, service: Any):
        """
        Register service.
        """
        self._services[name] = service
        return service

    # ===================================================================
    def resolve(self, name: str):
        """
        Resolve service.
        """
        return self._services.get(name)

    # ===================================================================

    def has(self, name: str):
        return name in self._services

    # ===================================================================

    def remove(self, name: str):
        self._services.pop(name, None)

    # ===================================================================

    def clear(self):
        self._services.clear()

    # ===================================================================

    def names(self):
        return sorted(self._services.keys())

    # ===================================================================

    def items(self):
        return self._services.items()

    # ===================================================================

    def __len__(self):
        return len(self._services)

    # ===================================================================

    def __contains__(self, item):
        return item in self._services

    # ===================================================================

    def __repr__(self):
        return (
            f"<ServiceContainer "
            f"services={len(self)}>"
        )


container = ServiceContainer()
