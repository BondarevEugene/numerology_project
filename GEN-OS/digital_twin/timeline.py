from dataclasses import dataclass,field


@dataclass
class TimelineProfile:
    current_age:int=0
    checkpoints:list=field(default_factory=list)
    roadmap:list=field(default_factory=list)
    milestones:list=field(default_factory=list)