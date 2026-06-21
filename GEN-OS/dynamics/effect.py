#Набор изменений.

from dataclasses import dataclass
from typing import List

from .modifier import Modifier


@dataclass
class Effect:
    modifiers: List[Modifier]

    duration: int = 0
