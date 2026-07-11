"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   GENESIS HR®                                                                ║
║──────────────────────────────────────────────────────────────────────────────║
║ MODULE      : Human Workspace Service                                        ║
║ FILE        : services/human_service.py                                      ║
║ LAYER       : Business Logic                                                 ║
║ BUILD       : 0500                                                           ║
║ STATUS      : ACTIVE                                                         ║
║                                                                              ║
║ Human Service                                                                ║
║ Central business service responsible for Digital Human Twin.                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

from services.base_service import BaseService

from services.career_service import career_service
from services.prediction_service import prediction_service
from services.development_service import development_service

from models.human import (
    DashboardCard,
    HumanProfile,
    HumanWorkspace,
    Competency,
    ProfessionRecommendation,
    HumanRisk,
    RoadmapStep,
    HumanSummary
)


class HumanWorkspaceService(BaseService):

    def __init__(self):
        super().__init__()
        self.name = "Human"
        self.boot()

    # ==========================================================
    # PROFILE
    # ==========================================================

    def load_profile(self) -> HumanProfile:
        forecast = prediction_service.forecast(None)
        return HumanProfile(
            fullname="Subject",
            archetype="Explorer",
            potential=84,
            market_fit=76,
            future_score=forecast["growth"]
        )

    # ==========================================================
    # DASHBOARD
    # ==========================================================

    def load_dashboard(self):
        profile = self.load_profile()
        forecast = prediction_service.forecast(profile)
        return [
            DashboardCard(
                title="Potential",
                value=str(profile.potential),
                subtitle="Overall Index",
                icon="🧠"
            ),

            DashboardCard(
                title="Career",
                value=str(profile.market_fit),
                subtitle="Market Fit",
                icon="💼"
            ),

            DashboardCard(
                title="Future",
                value=str(forecast["growth"]),
                subtitle="Prediction",
                icon="📈"
            ),

            DashboardCard(
                title="Success",
                value=str(forecast["success"]),
                subtitle="Forecast",
                icon="⭐"
            )
        ]

    # ==========================================================
    # COMPETENCIES
    # ==========================================================

    def load_top_competencies(self):
        return [
            Competency(
                name="Leadership",
                score=92
            ),
            Competency(
                name="Systems Thinking",
                score=88
            ),
            Competency(
                name="Communication",
                score=86
            ),

            Competency(
                name="Strategy",
                score=84
            ),
            Competency(
                name="Learning",
                score=83
            )
        ]

    # ==========================================================
    # RISKS
    # ==========================================================

    def load_risks(self):
        return [
            HumanRisk(
                title="Burnout",
                value=34,
                level="Medium"
            ),
            HumanRisk(
                title="Automation",
                value=18,
                level="Low"
            ),
            HumanRisk(
                title="Skill Gap",
                value=22,
                level="Medium"
            ),
            HumanRisk(
                title="Market Change",
                value=27,
                level="Medium"
            )
        ]
    # ==========================================================
    # PROFESSIONS
    # ==========================================================

    def load_recommended_professions(self):
        result = []
        for profession in career_service.professions():
            result.append(
                ProfessionRecommendation(
                    title=profession["title"],
                    score=profession["score"]
                )
            )
        return result

    # ==========================================================
    # ROADMAP
    # ==========================================================

    def load_roadmap(self):
        roadmap = []
        for step in development_service.roadmap():
            if isinstance(step, RoadmapStep):
                roadmap.append(step)
            else:
                roadmap.append(
                    RoadmapStep(
                        title=str(step),
                        description="",
                        completed=False
                    )
                )
        return roadmap

        # ==========================================================
        # SUMMARY
        # ==========================================================

    def summary(self) -> HumanSummary:
        profile = self.load_profile()
        return HumanSummary(
            total=1,
            active=1,
            average_potential=profile.potential,
            average_market_fit=profile.market_fit,
            updated="just now"
        )

        # ==========================================================
        # DATA ACCESS
        # ==========================================================

    def all(self):
        return [
            self.load_profile()
            ]

    def get(self, human_id: str):
        return self.load_profile()

    def exists(self, human_id: str):
        return True

    def search(self, query: str):
        if not query:
            return []
        profile = self.load_profile()
        query = query.lower()
        if (
            query in profile.fullname.lower()
            or
            query in profile.archetype.lower()

        ):
            return [
                profile
            ]
        return []

        # ==========================================================
        # DASHBOARD
        # ==========================================================

    def dashboard(self):
        return self.load_dashboard()

        # ==========================================================
        # WORKSPACE
        # ==========================================================

    def workspace(self) -> HumanWorkspace:
        return HumanWorkspace(
            profile=self.load_profile(),
            dashboard=self.load_dashboard(),
            competencies=self.load_top_competencies(),
            professions=self.load_recommended_professions(),
            risks=self.load_risks(),
            roadmap=self.load_roadmap()
        )

        # ==========================================================
        # EXPORT
        # ==========================================================

    def export(self):
        return self.workspace()

        # ==========================================================
        # STATISTICS
        # ==========================================================

    def statistics(self):
        summary = self.summary()
        return {
            "humans": summary.total,
            "active": summary.active,
            "average_potential": summary.average_potential,
            "average_market_fit": summary.average_market_fit,
            "updated": summary.updated,
            "competencies": len(
                self.load_top_competencies()
            ),
            "professions": len(
                self.load_recommended_professions()
            ),
            "risks": len(
                self.load_risks()
            ),
            "roadmap": len(
                self.load_roadmap()
            )
        }

        # ==========================================================
        # HEALTH
        # ==========================================================

    def health(self):
        return {
            "service": self.name,
            "ready": self.ready(),
            "objects": len(
                self.all()
            )
        }

    # ==========================================================
    # DEBUG
    # ==========================================================

    def __repr__(self):
        return (
            f"<HumanWorkspaceService "
            f"loaded={self.ready()}>"
        )


# ==========================================================
# SINGLETON
# ==========================================================

human_service = HumanWorkspaceService()
