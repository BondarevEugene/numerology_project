"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
Console Controller
BUILD-0024
Назначение
-----------
Управляет системной консолью GENOS.
Консоль является единым журналом событий платформы.
Источники сообщений:

• Workspace
• Registry
• Import
• AI
• Simulation
• Prediction
• Kernel

═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class ConsoleMessage:
    time: str
    level: str
    source: str
    message: str


class ConsoleController:
    MAX_MESSAGES = 500

    def __init__(self):
        self.messages: List[ConsoleMessage] = []
        self.info(
            "Kernel",
            "Genesis Console initialized."
        )

    def _timestamp(self):
        return datetime.now().strftime("%H:%M:%S")

    def add(
            self,
            source: str,
            message: str,
            level: str = "INFO"
    ):
        self.messages.append(
            ConsoleMessage(
                time=self._timestamp(),
                level=level,
                source=source,
                message=message
            )
        )
        if len(self.messages) > self.MAX_MESSAGES:
            self.messages.pop(0)

    def info(
            self,
            source: str,
            message: str
    ):
        self.add(
            source,
            message,
            "INFO"

        )

    def warning(
            self,
            source: str,
            message: str
    ):
        self.add(
            source,
            message,
            "WARNING"
        )

    def error(
            self,
            source: str,
            message: str
    ):
        self.add(
            source,
            message,
            "ERROR"
        )

    def success(
            self,
            source: str,
            message: str
    ):
        self.add(
            source,
            message,
            "SUCCESS"
        )

    def clear(self):
        self.messages.clear()

    def last(self, count=50):
        return self.messages[-count:]

    def context(self):
        return {
            "console": self.last()
        }
