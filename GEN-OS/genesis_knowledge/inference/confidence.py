"""
==========================================================
GENESIS HR®
Confidence Calculator
==========================================================
"""


class ConfidenceCalculator:

    @staticmethod
    def calculate(
            matches,
            total
    ):
        if total == 0:
            return 0
        return round(
            matches / total,
            2
        )
