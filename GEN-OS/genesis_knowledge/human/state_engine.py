"""
GENESIS HR®

State Engine
"""


class StateEngine:

    def __init__(self, registry):
        self.registry = registry

    def apply(
            self,
            code,
            delta
    ):
        variable = self.registry.get(code)
        if variable is None:
            return
        variable.value += delta
        variable.value = max(
            variable.minimum,
            variable.value
        )
        variable.value = min(
            variable.maximum,
            variable.value
        )
