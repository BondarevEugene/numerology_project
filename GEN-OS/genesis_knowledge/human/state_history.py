"""
GENESIS HR®

State History
"""


class StateHistory:

    def __init__(self):
        self.history = []

    def add(self, snapshot):
        self.history.append(snapshot)
