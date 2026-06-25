from dataclasses import dataclass,field


@dataclass
class CognitionProfile:

    archetypes:list=field(default_factory=list)
    thinking_style:str=""
    intelligence:list=field(default_factory=list)
    dominant_functions:list=field(default_factory=list)
    motivation:list=field(default_factory=list)
    values:list=field(default_factory=list)
