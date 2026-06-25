"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®

Simulation Controller

BUILD:0104

═══════════════════════════════════════════════════════════════════════
"""

from flask import render_template


class SimulationController:

    def workspace(self):

        return render_template(
            "workspaces/simulation_workspace.html"
        )

    def simulate(
        self,
        payload
    ):

        return {

            "success_probability": 87,

            "risk": 14,

            "timeline": 36
        }


simulation_controller = SimulationController()