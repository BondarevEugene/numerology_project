"""
═══════════════════════════════════════════════════════════════════════
Salary Service
BUILD:0130
═══════════════════════════════════════════════════════════════════════
"""


class SalaryService:

    def estimate(self, profession):

        return {
            "min":
                1500,
            "avg":
                3000,
            "max":
                6000
        }


salary_service = SalaryService()