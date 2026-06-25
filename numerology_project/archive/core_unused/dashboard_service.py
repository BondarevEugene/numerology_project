class DashboardService:

    @staticmethod
    def build(user=None):

        return {
            "show_history": bool(user),
            "show_subscription": bool(user),
            "show_pdf_export": bool(user)
        }