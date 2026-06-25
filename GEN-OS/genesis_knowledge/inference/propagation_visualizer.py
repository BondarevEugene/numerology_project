"""
═══════════════════════════════════════════════════════════════
GENESIS HR®

Propagation Visualizer
═══════════════════════════════════════════════════════════════
"""


class PropagationVisualizer:

    @staticmethod

    def render(result):

        lines=[]

        for event in result.events:

            lines.append(

                f"{event.source} "

                f"--{event.relation}--> "

                f"{event.target} "

                f"({event.value:+.2f})"

            )

        return "\n".join(lines)