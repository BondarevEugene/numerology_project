from dataclasses import dataclass,field


@dataclass
class PredictionProfile:

    career:list=field(default_factory=list)
    risks:list=field(default_factory=list)
    opportunities:list=field(default_factory=list)
    probability:float=0