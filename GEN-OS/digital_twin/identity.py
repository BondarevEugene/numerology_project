from __future__ import annotations

from dataclasses import dataclass


@dataclass
class IdentityProfile:

    person_id:int|None=None
    full_name:str=""
    birth_date:str=""
    gender:str=""
    country:str=""
    language:str=""
    timezone:str=""
