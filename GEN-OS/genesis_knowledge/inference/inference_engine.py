"""
==========================================================
GENESIS HR®
Inference Engine

==========================================================
"""

from .rule_executor import RuleExecutor


class InferenceEngine:

    def __init__(
            self,
            registry
    ):
        self.registry = registry
        self.executor = RuleExecutor()

    def infer(
            self,
            profile
    ):
        return self.executor.execute(
            profile,
            self.registry.enabled()
        )
