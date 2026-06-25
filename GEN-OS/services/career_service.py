"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®

Career Service

BUILD:0129
═══════════════════════════════════════════════════════════════════════
"""


class CareerService:

    def professions(self):

        return [

            {
                "title":
                    "Project Manager",

                "score":
                    94
            },

            {
                "title":
                    "Business Analyst",

                "score":
                    91
            }

        ]

    def top_match(self):

        return {

            "title":
                "Project Manager",

            "score":
                94

        }


career_service = CareerService()