/*
═══════════════════════════════════════════════════════════════════════

GENESIS HR®

Toolbar Controller

BUILD 0300

Главная панель управления платформой.

Все действия проходят через Genesis EventBus.

═══════════════════════════════════════════════════════════════════════
*/

class Toolbar {

    constructor() {

        this.buttons = [];

        this.tabs = [];

        this.initialized = false;

    }

    /*
    ==========================================================
    INITIALIZE
    ==========================================================
    */

    initialize() {

        if (this.initialized) {
            return;
        }

        this.initialized = true;

        this.buttons = Array.from(
            document.querySelectorAll(
                "[data-toolbar-action]"
            )
        );

        this.tabs = Array.from(
            document.querySelectorAll(
                "[data-workspace]"
            )
        );

        this.bindButtons();

        this.bindWorkspaces();

        console.log("[Toolbar] Ready");

    }

    /*
    ==========================================================
    TOOLBAR BUTTONS
    ==========================================================
    */

    bindButtons() {

        this.buttons.forEach(button => {

            button.addEventListener("click", () => {

                this.execute(

                    button.dataset.toolbarAction

                );

            });

        });

    }

    /*
    ==========================================================
    WORKSPACE BUTTONS
    ==========================================================
    */

    bindWorkspaces() {

        this.tabs.forEach(tab => {

            tab.addEventListener("click", () => {

                this.openWorkspace(

                    tab.dataset.workspace

                );

            });

        });

    }

    /*
    ==========================================================
    OPEN WORKSPACE
    ==========================================================
    */

    openWorkspace(workspace) {

        if (!workspace)
            return;

        this.tabs.forEach(tab => {

            tab.classList.remove("active");

            if (

                tab.dataset.workspace === workspace

            ) {

                tab.classList.add("active");

            }

        });

        console.log(

            "[Toolbar] Workspace:",

            workspace

        );

        if (window.bus) {

            window.bus.emit(

                "workspace.change",

                {

                    workspace

                }

            );

        }

    }

    /*
    ==========================================================
    TOOLBAR ACTION
    ==========================================================
    */

    execute(action) {

        if (!action)
            return;

        console.log(

            "[Toolbar]",

            action

        );

        if (window.bus) {

            window.bus.emit(

                "toolbar.action",

                {

                    action

                }

            );

        }

    }

    /*
    ==========================================================
    REFRESH
    ==========================================================
    */

    refresh() {

        this.buttons = Array.from(

            document.querySelectorAll(

                "[data-toolbar-action]"

            )

        );

        this.tabs = Array.from(

            document.querySelectorAll(

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

window.toolbar = new Toolbar();
