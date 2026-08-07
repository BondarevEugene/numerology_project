/*
═══════════════════════════════════════════════════════════════════════

GENESIS EVENT BUS

BUILD 0400

═══════════════════════════════════════════════════════════════════════
*/

class EventBus {

    emit(event, payload = {}) {

        document.dispatchEvent(

            new CustomEvent(

                event,

                {

                    detail: payload

                }

            )

        );

    }

    on(event, callback) {

        document.addEventListener(

            event,

            callback

        );

    }

    once(event, callback) {

        const handler = (e) => {

            callback(e);

            document.removeEventListener(

                event,

                handler

            );

        };

        document.addEventListener(

            event,

            handler

        );

    }

    off(event, callback) {

        document.removeEventListener(

            event,

            callback

        );

    }

}

window.bus =

    new EventBus();