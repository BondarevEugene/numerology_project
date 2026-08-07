"""
═══════════════════════════════════════════════════════════════════════════════

 GENESIS HR® // OMNIFACTORY EVO

 MODULE
-----------------------------------------------------------------------------
 Module Loader

 FILE
-----------------------------------------------------------------------------
 module_loader.py

 BUILD
-----------------------------------------------------------------------------
 0157

 DESCRIPTION
-----------------------------------------------------------------------------

 Discovers, loads and initializes
 GEN-OS Kernel Modules.

 Every platform module should expose:

    module.py

containing

    class Module(KernelModule)

═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import importlib
import logging
import pkgutil

LOGGER = logging.getLogger(
    "GEN-OS.ModuleLoader"
)


class ModuleLoader:

    """
    Platform Module Loader.
    """

    def __init__(self):

        self._modules = []

    # ============================================================
    # DISCOVERY
    # ============================================================

    def discover(
        self,
        package
    ):

        """
        Discover python modules.
        """

        modules = []

        for _, name, _ in pkgutil.iter_modules(
            package.__path__
        ):

            module = importlib.import_module(

                f"{package.__name__}.{name}"

            )

            modules.append(module)

        return modules

    # ============================================================
    # LOADING
    # ============================================================

    def load(
        self,
        module
    ):

        """
        Register loaded module.
        """

        LOGGER.info(

            "Loaded module %s",

            module.__name__

        )

        self._modules.append(module)

        return module

    # ------------------------------------------------------------

    def load_all(
        self,
        package
    ):

        """
        Discover and load every module.
        """

        discovered = self.discover(
            package
        )

        for module in discovered:

            self.load(module)

        return self._modules

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def initialize(
        self,
        kernel
    ):

        """
        Initialize modules.
        """

        for module in self._modules:

            module_class = getattr(

                module,

                "Module",

                None

            )

            if module_class is None:

                continue

            instance = module_class()

            instance.register_services(
                kernel
            )

            instance.register_events(
                kernel
            )

            instance.register_workspaces(
                kernel
            )

            instance.initialize()

    # ============================================================
    # INFORMATION
    # ============================================================

    def modules(self):

        return self._modules

    # ------------------------------------------------------------

    def count(self):

        return len(
            self._modules
        )

    # ------------------------------------------------------------

    def information(self):

        return {

            "modules": self.count()

        }

    # ------------------------------------------------------------

    def __len__(self):

        return self.count()

    # ------------------------------------------------------------

    def __repr__(self):

        return (

            "<ModuleLoader "

            f"modules={self.count()}>"

        )


module_loader = ModuleLoader()