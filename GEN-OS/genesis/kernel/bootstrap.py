"""
═══════════════════════════════════════════════════════════════════════════════
GENESIS HR®

GEN-OS Platform

FILE:bootstrap.py

BUILD:0022

DESCRIPTION

Platform Bootstrap.
Запускает платформу.

Инициализирует:
• Kernel
• Services
• Modules
• Workspaces

После выполнения boot()
вся система считается готовой
к работе.

═══════════════════════════════════════════════════════════════════════════════
"""

from genesis.kernel.genesis_kernel import GenesisKernel
from genesis.kernel.service_container import ServiceContainer
from genesis.kernel.module_manager import ModuleManager
from genesis.kernel.workspace_manager import WorkspaceManager


class Bootstrap:

    """
    Главный загрузчик платформы.
    """

    def __init__(self):
        self.kernel = GenesisKernel()

    # ======================================================
    # START
    # ======================================================

    def boot(self):
        print()
        print("════════════════════════════════════")
        print(" GENESIS HR")
        print(" Boot sequence")
        print("════════════════════════════════════")

        self.kernel.container = ServiceContainer()
        print("[ OK ] Service Container")
        self.kernel.modules = ModuleManager()
        self.kernel.modules.register_default_modules()
        print("[ OK ] Module Manager")
        self.kernel.workspaces = WorkspaceManager()
        self.kernel.workspaces.register_default_workspaces()
        print("[ OK ] Workspace Manager")
        self.kernel.health_check()
        print("[ OK ] Health Monitor")
        print()
        print("Platform Ready")
        print()
        return self.kernel

    # ======================================================
    # INFO
    # ======================================================

    def information(self):
        return {
            "version":
                self.kernel.VERSION,
            "modules":
                self.kernel.modules.count,
            "workspaces":
                self.kernel.workspaces.count,
            "services":
                self.kernel.container.count
        }


_bootstrap = Bootstrap()


def boot():
    return _bootstrap.boot()


def kernel():
    return _bootstrap.kernel
