"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
Human Domain Models
═══════════════════════════════════════════════════════════════════════
"""
from __future__ import annotations
from dataclasses import dataclass
from dataclasses import field


# ==========================================================
# DASHBOARD
# ==========================================================

@dataclass(slots=True)
class DashboardCard:
    title: str
    value: str
    subtitle: str
    icon: str

# ==========================================================
# COMPETENCY
# ==========================================================

@dataclass(slots=True)
class Competency:
    name: str
    score: int
    category: str = ""
    trend: str = ""
    description: str = ""

# ==========================================================
# PROFESSION
# ==========================================================

@dataclass(slots=True)
class ProfessionRecommendation:
    title: str
    score: int
    salary: str = ""
    demand: str = ""
    description: str = ""


# ==========================================================
# RISK
# ==========================================================

@dataclass(slots=True)
class HumanRisk:
    title: str
    value: int
    level: str = "LOW"
    description: str = ""


# ==========================================================
# TIMELINE
# ==========================================================

@dataclass(slots=True)
class RoadmapStep:
    title: str
    completed: bool = False
    duration: str = ""
    description: str = ""


# ==========================================================
# PROFILE
# ==========================================================

@dataclass(slots=True)
class HumanProfile:
    fullname: str
    archetype: str
    potential: int
    market_fit: int
    future_score: int

# ==========================================================
# SUMMARY
# ==========================================================

@dataclass(slots=True)
class HumanSummary:
    total: int
    active: int
    average_potential: float
    average_market_fit: float
    updated: str


# ==========================================================
# WORKSPACE
# ==========================================================

@dataclass(slots=True)
class HumanWorkspace:
    profile: HumanProfile
    dashboard: list[DashboardCard] = field(default_factory=list)
    competencies: list[Competency] = field(default_factory=list)
    professions: list[ProfessionRecommendation] = field(default_factory=list)
    risks: list[HumanRisk] = field(default_factory=list)
    roadmap: list[RoadmapStep] = field(default_factory=list)









