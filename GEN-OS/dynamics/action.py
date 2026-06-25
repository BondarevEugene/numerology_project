#Любое действие человека.

from dataclasses import dataclass

from .effect import Effect


@dataclass
class Action:
    id: str
    title: str
    category: str
    effect: Effect
    energy_cost: int = 0
    time_cost: int = 0
