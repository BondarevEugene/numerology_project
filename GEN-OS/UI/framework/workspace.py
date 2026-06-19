"""
═══════════════════════════════════════════════════════════════════════

                        GENESIS HR®

                 GENOS Workspace Framework

Module:
Workspace Engine

Description:
Главный контейнер рабочей среды.

═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Workspace:

    title: str

    modules: List = field(default_factory=list)

    windows: List = field(default_factory=list)

    status = "READY"

    version = "0.4 Alpha"

    def add_module(self, module):

        self.modules.append(module)

    def add_window(self, window):

        self.windows.append(window)

    def remove_window(self, window_id):

        self.windows = [

            w for w in self.windows

            if w.id != window_id

        ]