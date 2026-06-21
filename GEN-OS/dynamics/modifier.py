#Модификатор изменения.

from dataclasses import dataclass


@dataclass
class Modifier:
    variable: str

    delta: float

    source: str = ""
