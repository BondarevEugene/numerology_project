"""
═══════════════════════════════════════════════════════════════

GENESIS®

Event Bus

BUILD 0106

═══════════════════════════════════════════════════════════════
"""

from collections import defaultdict


class EventBus:

    def __init__(self):

        self.listeners = defaultdict(list)

    def on(self, event, callback):

        self.listeners[event].append(callback)

    def emit(self, event, payload=None):

        if payload is None:
            payload = {}

        for callback in self.listeners[event]:

            callback(payload)

    def clear(self):

        self.listeners.clear()


bus = EventBus()