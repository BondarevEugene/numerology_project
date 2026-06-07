from core.session_history_service import (
    SessionHistoryService
)


class ProfileDashboardService:

    @staticmethod
    def build(
        user_id
    ):

        history = (
            SessionHistoryService
            .get_user_history(
                user_id
            )
        )

        return {
            "history": history,
            "reports_count": len(
                history
            )
        }