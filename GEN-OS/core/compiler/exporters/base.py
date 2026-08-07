from pathlib import Path
from abc import ABC, abstractmethod


class BaseExporter(ABC):
    """
    Базовый класс всех Exporter.
    """
    filename: str = ""

    @abstractmethod
    def generate(
            self,
            project_path: Path
    ):
        """
        Создать файл.
        """
        raise NotImplementedError

