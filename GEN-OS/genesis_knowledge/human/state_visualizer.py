"""
GENESIS HR®

State Visualizer
"""


class StateVisualizer:

    @staticmethod
    def render(registry):
        lines = []
        for item in registry.all():
            lines.append(
                f"{item.title:<24}"
                f"{item.value:>6.1f}"
            )
        return "\n".join(lines)
