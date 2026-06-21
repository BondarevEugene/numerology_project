"""
==========================================================
GENESIS HR®
Rule Executor
==========================================================
"""


class RuleExecutor:

    def execute(
            self,
            profile,
            rules
    ):
        result = []
        for rule in rules:
            if self.match(
                    profile,
                    rule.condition
            ):
                result.append(
                    rule.action
                )
        return result

    def match(
            self,
            profile,
            condition
    ):
        for key, value in condition.items():
            if profile.get(key) != value:
                return False
        return True
