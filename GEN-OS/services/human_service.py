"""
═══════════════════════════════════════════════════════════════════════════════
GENESIS HR®

GEN-OS Platform

FILE:
human_service.py

BUILD:
0043

DESCRIPTION
Human Workspace Service.

Собирает цифровой профиль человека.

Является центральной точкой,
из которой Workspace получает данные.

Позже сюда будут подключены:

• Numerology Engine
• Archetype Engine
• Career Engine
• AI Matching
• Prediction Engine
• Development Engine

═══════════════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass
from typing import List


@dataclass
class DashboardCard:

    title: str

    value: str

    subtitle: str

    icon: str


@dataclass(slots=True)
class HumanProfile:

    fullname: str

    archetype: str

    potential: int

    market_fit: int

    future_score: int


class HumanWorkspaceService:

    def load_dashboard(self):

        return [

            DashboardCard(

                title="Potential",

                value="84",

                subtitle="Overall Index",

                icon="🧠"

            ),

            DashboardCard(

                title="Career",

                value="76",

                subtitle="Market Fit",

                icon="💼"

            ),

            DashboardCard(

                title="Future",

                value="91",

                subtitle="Prediction",

                icon="📈"

            ),

            DashboardCard(

                title="Growth",

                value="88",

                subtitle="Development",

                icon="🚀"

            )

        ]

    def load_profile(self):

        return HumanProfile(

            fullname="Subject",

            archetype="Explorer",

            potential=84,

            market_fit=76,

            future_score=91

        )

    def load_top_competencies(self):

        return [

            ("Leadership",92),

            ("Systems Thinking",88),

            ("Communication",86),

            ("Strategy",84),

            ("Learning",83)

        ]

    def load_recommended_professions(self):

        return [

            ("Project Manager",94),

            ("Product Owner",91),

            ("Business Analyst",89),

            ("Operations Director",87),

            ("Solution Architect",86)

        ]

    def load_risks(self):

        return [

            ("Burnout",34),

            ("Automation",18),

            ("Skill Gap",22),

            ("Market Change",27)

        ]

    def load_roadmap(self):

        return [

            "Systems Thinking",

            "Leadership",

            "Business Analytics",

            "Negotiation",

            "AI Literacy"

        ]