#Это цифровой снимок человека.
from dataclasses import dataclass
from typing import Dict

@dataclass

class HumanState:

    variables:Dict[str,float]