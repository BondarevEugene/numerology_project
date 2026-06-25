"""
==========================================================
GENESIS HR®
Rule Registry
==========================================================
"""


class RuleRegistry:

    def __init__(self):
        self.rules = []

    def add(self, rule):
        self.rules.append(rule)

    def all(self):
        return self.rules

    def enabled(self):
        return [
            rule
            for rule in self.rules
            if rule.enabled
        ]

    def count(self):
        return len(self.rules)
