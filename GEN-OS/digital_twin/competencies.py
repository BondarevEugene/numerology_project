from dataclasses import dataclass,field


@dataclass
class CompetencyProfile:

    competencies:list=field(default_factory=list)
    strengths:list=field(default_factory=list)
    weaknesses:list=field(default_factory=list)
    leadership:int=0
    communication:int=0
    analytics:int=0
    creativity:int=0
    management:int=0
