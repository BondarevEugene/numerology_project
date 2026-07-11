/*
╔══════════════════════════════════════════════════════════════════════════════╗
║ GENESIS HR®                                                                  ║
║ STATE MANAGER                                                                ║
║ BUILD 0400                                                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
*/

class StateManager {

    constructor() {

        this.data = {

            workspace: "dashboard",

            theme: "dark",

            explorer: true,

            inspector: true,

            console: false,

            loading: false,

            online: true

        };

    }

    get(key) {

        return this.data[key];

    }

    set(key, value) {

        this.data[key] = value;

        if (window.bus) {

            window.bus.emit(

                "state.changed",

                {

                    key,

                    value

                }

            );

        }

    }

    toggle(key) {

        this.set(

            key,

            !this.get(key)

        );

    }

    update(values) {

        Object.assign(

            this.data,

            values

        );

    }

    snapshot() {

        return {

            ...this.data

        };

    }

    restore(snapshot) {

        this.data = {

            ...snapshot

        };

    }

}

window.state =

    new StateManager();