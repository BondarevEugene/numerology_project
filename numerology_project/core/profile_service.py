from core.session_history_service import (
    SessionHistoryService
)


class ProfileService:

    @staticmethod
    def build(user):

        history = (
            SessionHistoryService
            .get_user_history(
                user.id
            )
        )

        return {
            "user": user,
            "history": history,
            "reports_count": len(
                history
            ),
            "subscription": "FREE"
        }