class CareerService:
    """
    Работа с профессиями и карьерными рекомендациями.
    """

    @staticmethod
    def get_recommendations(result_data):

        jobs = result_data.get("jobs", [])

        return jobs