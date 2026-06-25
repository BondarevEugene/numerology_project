"""
═══════════════════════════════════════════════════════════════
GENESIS HR®

Propagation Statistics
═══════════════════════════════════════════════════════════════
"""


class PropagationStatistics:

    @staticmethod

    def build(result):

        return{

            "events":len(result.events),

            "entities":len(result.updated_entities)

        }