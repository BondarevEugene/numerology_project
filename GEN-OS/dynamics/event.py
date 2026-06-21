#Любое событие.
from dataclasses import dataclass

@dataclass

class Event:

    id:str

    title:str

    payload:dict