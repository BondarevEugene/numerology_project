"""
═══════════════════════════════════════════════════════════════════════════════

 GENESIS HR® // OMNIFACTORY EVO

 MODULE
-----------------------------------------------------------------------------
 Knowledge Module

 FILE
-----------------------------------------------------------------------------
 module.py

 BUILD
-----------------------------------------------------------------------------
 0161

 DESCRIPTION
-----------------------------------------------------------------------------

 Knowledge Module объединяет все подсистемы знаний.

 Содержит:

    • Knowledge Registry

    • Knowledge Graph

    • Knowledge Services

═══════════════════════════════════════════════════════════════════════════════
"""

from kernel.module import KernelModule

from registry.knowledge_registry import knowledge_registry

from services.knowledge_graph_service import knowledge_graph_service
from services.knowledge_service import knowledge_service


class Module(KernelModule):

    NAME = "Knowledge"

    VERSION = "1.0.0"

    BUILD = "0161"

    DESCRIPTION = "Knowledge Infrastructure"

    # ============================================================
    # SERVICES
    # ============================================================

    def register_services(
        self,
        kernel
    ):

        kernel.registry.register(

            type(knowledge_registry),

            knowledge_registry

        )

        kernel.registry.register(

            type(knowledge_graph_service),

            knowledge_graph_service

        )

        kernel.registry.register(

            type(knowledge_service),

            knowledge_service

        )

    # ============================================================
    # EVENTS
    # ============================================================

    def register_events(
        self,
        kernel
    ):

        pass

    # ============================================================
    # WORKSPACES
    # ============================================================

    def register_workspaces(
        self,
        kernel
    ):

        pass

    # ============================================================
    # INITIALIZE
    # ============================================================

    def initialize(
        self
    ):

        knowledge_graph_service.attach_registry(
            knowledge_registry
        )

        knowledge_graph_service.build_from_registry()
