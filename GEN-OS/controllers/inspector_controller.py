"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
Inspector Controller
BUILD-0024
Назначение
-----------
Управляет правой информационной панелью (Inspector).
Inspector показывает свойства выбранного объекта.
Сам ничего не вычисляет.
Получает объект от Registry и передает его GUI.

═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class InspectorField:
    title: str
    value: str


@dataclass
class InspectorSection:
    title: str
    fields: List[InspectorField] = field(default_factory=list)


class InspectorController:
    def __init__(self):
        self.sections = []

    def clear(self):
        self.sections = []

    def load_entity(self, entity):
        """
        Загружает объект Registry
        и превращает его в набор секций Inspector.
        """
        self.clear()
        if entity is None:
            return

        general = InspectorSection("General")
        general.fields.append(
            InspectorField(
                "Name",
                getattr(entity, "name", "")
            )
        )

        general.fields.append(
            InspectorField(
                "Type",
                getattr(entity, "entity_type", "")
            )
        )

        general.fields.append(
            InspectorField(
                "Identifier",
                getattr(entity, "id", "")
            )
        )

        self.sections.append(general)
        metadata = getattr(entity, "metadata", {})
        if metadata:
            section = InspectorSection("Metadata")
            for key, value in metadata.items():
                section.fields.append(
                    InspectorField(
                        str(key),
                        str(value)
                    )
                )
            self.sections.append(section)

    def context(self):
        return {
            "sections": self.sections
        }

    def has_selection(self):
        return len(self.sections) > 0
