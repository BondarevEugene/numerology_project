"""
==========================================================
GENESIS HR®
Scoring Engine
==========================================================
"""


class ScoreEngine:

    @staticmethod
    def weighted_score(
            values
    ):
        if not values:
            return 0
        total = 0
        weight = 0
        for score, w in values:
            total += score * w
            weight += w
        if weight == 0:
            return 0
        return round(total / weight, 2)
