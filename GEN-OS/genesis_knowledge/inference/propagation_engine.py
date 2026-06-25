"""
═══════════════════════════════════════════════════════════════
GENESIS HR®

Propagation Engine
═══════════════════════════════════════════════════════════════
"""

from .propagation_result import PropagationResult
from .propagation_event import PropagationEvent
from .propagation_rules import RULES


class PropagationEngine:

    def __init__(self,registry):

        self.registry=registry

    def propagate(self,start_entity):

        result=PropagationResult()

        for relation in self.registry.all():

            if relation.source!=start_entity:

                continue

            multiplier=RULES.get(

                relation.relation_type,

                0

            )

            value=relation.weight*multiplier

            result.events.append(

                PropagationEvent(

                    source=relation.source,

                    target=relation.target,

                    relation=relation.relation_type,

                    value=value

                )

            )

            result.updated_entities.append(

                relation.target

            )

            result.score_changes[

                relation.target

            ]=value

        return result