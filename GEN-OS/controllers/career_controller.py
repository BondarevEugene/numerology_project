"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®

Career Controller

BUILD:0127
═══════════════════════════════════════════════════════════════════════
"""

from flask import render_template


class CareerController:

    def workspace(self):

        return render_template(
            "workspaces/career_workspace.html"
        )

    def recommendations(self):

        return [

            {
                "title": "Project Manager",
                "score": 94
            },

            {
                "title": "Business Analyst",
                "score": 91
            },

            {
                "title": "Solution Architect",
                "score": 89
            }

        ]


career_controller = CareerController()