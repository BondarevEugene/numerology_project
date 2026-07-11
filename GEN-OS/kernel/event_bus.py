"""
═══════════════════════════════════════════════════════════════
Genesis Event Bus
BUILD 0600
═══════════════════════════════════════════════════════════════
"""


class EventBus:

    def __init__(self):
        self.listeners = {}

    # =====================================================

    def on(self, event, callback):
        self.listeners.setdefault(
            event,
            []
        ).append(callback)

    # =====================================================

    def off(self, event, callback):

        if event not in self.listeners:
            return

        if callback in self.listeners[event]:
            self.listeners[event].remove(callback)

    # =====================================================

    def emit(self, event, *args, **kwargs):

        for callback in self.listeners.get(
            event,
            []
        ):
            callback(
                *args,
                **kwargs
            )

    # =====================================================
    # Backward compatibility
    # =====================================================

    def publish(self, event, *args, **kwargs):
        """
        Старое API.

        Полностью совместимо.
        """
        return self.emit(
            event,
            *args,
            **kwargs
        )

    # =====================================================

    def subscribe(self, event, callback):
        """
        Старое API.
        """
        return self.on(
            event,
            callback
        )

    # =====================================================

    def unsubscribe(self, event, callback):
        """
        Старое API.
        """
        return self.off(
            event,
            callback
        )


event_bus = EventBus()