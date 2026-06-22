"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
GENESIS KERNEL
Event Bus
BUILD-0025
Назначение
-----------

Единая система обмена событиями между всеми подсистемами GENOS.

Подписчики:
• Workspace
• Explorer
• Inspector
• Registry
• Import
• AI
• Prediction
• Graph
• Simulation
• Console

═══════════════════════════════════════════════════════════════════════
"""

from collections import defaultdict
from typing import Callable, Dict, List


class EventBus:

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)

    def subscribe(
            self,
            event_name: str,
            callback: Callable
    ):
        if callback not in self._subscribers[event_name]:
            self._subscribers[event_name].append(callback)

    def unsubscribe(
            self,
            event_name: str,
            callback: Callable
    ):
        if callback in self._subscribers[event_name]:
            self._subscribers[event_name].remove(callback)

    def publish(
            self,
            event_name: str,
            payload=None
    ):
        listeners = self._subscribers.get(event_name, [])
        for callback in listeners:
            callback(payload)

    def clear(self):
        self._subscribers.clear()

    def statistics(self):
        return {
            name: len(callbacks)
            for name, callbacks
            in self._subscribers.items()
        }


event_bus = EventBus()
