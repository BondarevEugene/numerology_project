"""
Genesis Module Loader
"""

import importlib
import pkgutil


class ModuleLoader:

    def discover(self, package):
        modules = []
        for _, name, _ in pkgutil.iter_modules(
            package.__path__
        ):
            module = importlib.import_module(
                f"{package.__name__}.{name}"
            )
            modules.append(
                module
            )
        return modules


module_loader = ModuleLoader()