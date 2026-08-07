/*
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
Explorer Controller
BUILD 0300
Navigator Workspace
═══════════════════════════════════════════════════════════════════════
*/
class Explorer {
    constructor() {
        this.root = null;
        this.items = [];
        this.initialized = false;
    }

    /*
    ==========================================================
    INITIALIZE
    ==========================================================
    */

    initialize() {
        if (this.initialized)
            return;
        this.initialized = true;
        this.root = document.querySelector(".gen-explorer");
        if (!this.root) {
            console.warn(
                "[Explorer] Root not found."
            );
            return;
        }
        this.items = Array.from(
            this.root.querySelectorAll(
                "[data-workspace]"
            )
        );
        this.bind();
        console.log(
            "[Explorer] Ready"
        );
    }

    /*
    ==========================================================
    EVENTS
    ==========================================================
    */
    bind() {
        this.items.forEach(item => {
            item.addEventListener(
                "click",
                () => {
                    const workspace =
                        item.dataset.workspace;

                    this.activate(workspace);

                    if (window.bus) {

                        window.bus.emit(

                            "workspace.change",

                            {

                                workspace

                            }

                        );

                    }

                }

            );

        });

    }

    /*
    ==========================================================
    ACTIVE
    ==========================================================
    */

    activate(workspace) {

        this.items.forEach(item => {

            item.classList.remove(
                "active"
            );

            if (

                item.dataset.workspace === workspace

            ) {

                item.classList.add(
                    "active"
                );

            }

        });

    }

    /*
    ==========================================================
    API
    ==========================================================
    */

    refresh() {

        this.items = Array.from(

            this.root.querySelectorAll(

                "[data-workspace]"

            )

        );

    }

}

/*
==========================================================
GLOBAL
==========================================================
*/

window.explorer = new Explorer();