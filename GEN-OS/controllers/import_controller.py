"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
Import Controller
BUILD-0031
Author:
OpenAI + Yevhenii Bondariev
Description:
Управляет Import Station.
Функции:

• выбор файла
• предварительный просмотр
• запуск импорта
• история
• прогресс
• отмена

═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass
from typing import Optional

from controllers.console_controller import console
from controllers.statusbar_controller import statusbar


@dataclass
class ImportState:
    filename: str = ""
    provider: str = "excel"
    status: str = "Idle"
    progress: int = 0
    imported: int = 0
    failed: int = 0


class ImportController:

    def __init__(self):
        self.state = ImportState()

    def select_file(
        self,
        filename: str
    ):
        self.state.filename = filename
        console.info(
            "Import",
            f"Selected {filename}"
        )

    def set_provider(
        self,
        provider: str
    ):
        self.state.provider = provider

    def start(self):
        self.state.status = "Running"
        self.state.progress = 0
        statusbar.set_import_jobs(1)
        console.info(
            "Import",
            "Import started."
        )

    def update(
        self,
        progress: int
    ):
        self.state.progress = progress

    def finish(
        self,
        imported: int,
        failed: int
    ):
        self.state.status = "Completed"
        self.state.progress = 100
        self.state.imported = imported
        self.state.failed = failed
        statusbar.set_import_jobs(0)
        console.success(
            "Import",
            f"{imported} imported."
        )

    def error(
        self,
        message: str
    ):
        self.state.status = "Error"
        statusbar.set_import_jobs(0)
        console.error(
            "Import",
            message
        )

    def context(self):
        return {
            "import": self.state
        }


import_controller = ImportController()