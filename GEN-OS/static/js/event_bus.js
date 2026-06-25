/*
═══════════════════════════════════════════════════════════════════════
Event Bus

BUILD:0122
═══════════════════════════════════════════════════════════════════════
*/

class EventBus {

    emit(
        event,
        payload = {}
    ) {

        document.dispatchEvent(
            new CustomEvent(
                event,
                {
                    detail:
                        payload
                }
            )
        );
    }

    on(
        event,
        callback
    ) {

        document.addEventListener(
            event,
            callback
        );
    }
}

window.eventBus =
    new EventBus();