from dataclasses import dataclass


#Каждая изменяемая характеристика человека.


@dataclass
class Variable:
    code: str
    title: str
    value: float = 0
    minimum: float = 0
    maximum: float = 100
