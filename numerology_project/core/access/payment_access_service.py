class PaymentAccessService:

    @staticmethod
    def has_premium_access(user=None):

        if not user:
            return False

        if getattr(
            user,
            "is_nexus_admin",
            False
        ):
            return True

        return getattr(
            user,
            "subscription_active",
            False
        )