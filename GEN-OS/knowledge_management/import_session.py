"""
═══════════════════════════════════════════════════════════════════════════════

GENESIS HR® // GEN-OS

Knowledge Management Core

FILE:
import_session.py

BUILD:
0101

DESCRIPTION:

Контейнер жизненного цикла импорта данных.

Каждая операция загрузки набора данных представляет собой отдельную
Import Session.

Сессия хранит:

• источник данных
• пользователя
• состояние
• количество строк
• ошибки
• предупреждения
• журнал выполнения

Import Session используется всеми последующими сервисами платформы.

Validation Engine

Normalization Engine

Registry Loader

Knowledge Graph Builder

Prediction Engine

═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ImportStatus(str, Enum):

    CREATED = "created"

    LOADING = "loading"

    VALIDATING = "validating"

    NORMALIZING = "normalizing"

    IMPORTING = "importing"

    BUILDING_GRAPH = "building_graph"

    COMPLETED = "completed"

    FAILED = "failed"


@dataclass(slots=True)
class ImportSession:

    session_id: str

    dataset_name: str

    source_name: str

    created_by: str

    created_at: datetime = field(default_factory=datetime.utcnow)

    status: ImportStatus = ImportStatus.CREATED

    total_rows: int = 0

    processed_rows: int = 0

    imported_nodes: int = 0

    imported_edges: int = 0

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    log: list[str] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    def add_log(self, message: str):

        timestamp = datetime.utcnow().strftime("%H:%M:%S")

        self.log.append(f"[{timestamp}] {message}")

    def add_warning(self, message: str):

        self.warnings.append(message)

        self.add_log(f"WARNING :: {message}")

    def add_error(self, message: str):

        self.errors.append(message)

        self.status = ImportStatus.FAILED

        self.add_log(f"ERROR :: {message}")

    def set_status(self, status: ImportStatus):

        self.status = status

        self.add_log(f"STATUS → {status.value}")