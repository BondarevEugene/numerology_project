/*
═══════════════════════════════════════════════════════════════════════

GENESIS HR®

GEN-OS Workspace Loader

BUILD 0300

Workspace Loader отвечает только за:

• загрузку Workspace
• кэширование
• вставку HTML
• вызов WorkspaceInit()

═══════════════════════════════════════════════════════════════════════
*/

class WorkspaceLoader {

    constructor() {

        this.current = null;

        this.cache = {};

        this.container = null;

    }

    /*
    =========================================================
    INIT
    =========================================================
    */

initialize() {

    this.container = document.getElementById("workspace-container");
    if (!this.container) {
        console.error(
            "[WorkspaceLoader] #workspace-container not found."
        );
        return;
    }
    if (window.bus) {
        window.bus.on(
            "workspace.change",
            payload => {
                this.open(
                    payload.workspace
                );
            }
        );
    }

    console.log(
        "[WorkspaceLoader] Ready"
    );

}

        /*
        EventBus
        */

        if (window.bus) {

            window.bus.on(

                "workspace.change",

                payload => {

                    this.open(
                        payload.workspace
                    );

                }

            );

        }

        this.open("human");

    }

    /*
    =========================================================
    OPEN
    =========================================================
    */

    async open(name) {

        if (!name)
            return;

        if (this.current === name)
            return;

        if (!this.container)
            return;

        console.log("[Workspace] Opening:", name);
        this.loading();

        try {

            let html;

            if (this.cache[name]) {

                html = this.cache[name];

            }

            else {

                const response =
                    await fetch(
                        `/workspace/${name}`
                    );

                if (!response.ok)
                    throw new Error(
                        response.statusText
                    );

                html =
                    await response.text();

                this.cache[name] = html;

            }

            this.container.innerHTML = html;
            window.dispatchEvent(
                new CustomEvent(
                    "workspace.loaded",
                    {
                        detail: {
                            workspace: name
                    }
                }
            )
        );
            this.current = name;
            this.initializeWorkspace(name);
            window.Genesis.emit(
                "workspace.loaded",
                {
                    workspace: name
                }
            );
        }

        catch (e) {

            console.error(e);

            this.error(e);

        }

    }

    /*
    =========================================================
    ACTIVATE MENU
    =========================================================
    */

    activate(name) {

        document

            .querySelectorAll(
                "[data-workspace]"
            )

            .forEach(item => {

                item.classList.remove(
                    "active"
                );

                if (

                    item.dataset.workspace ===
                    name

                ) {

                    item.classList.add(
                        "active"
                    );

                }

            });

    }

    /*
    =========================================================
    WORKSPACE INIT
    =========================================================
    */

    initializeWorkspace(name) {

        const fn =
            window[
                `${name}WorkspaceInit`
            ];

        if (

            typeof fn ===
            "function"

        ) {

            fn();

        }

    }

    /*
    =========================================================
    LOADING
    =========================================================
    */

    loading() {

        this.container.innerHTML = `

<div class="gen-loading">

<div class="gen-spinner"></div>

<div class="gen-loading-text">

Loading Workspace...

</div>

</div>

`;

    }

    /*
    =========================================================
    ERROR
    =========================================================
    */

    error(error) {

        this.container.innerHTML = `

<div class="gen-error">

<h2>

Workspace Error

</h2>

<p>

${error.message}

</p>

</div>

`;

    }

}

window.workspaceLoader =
    new WorkspaceLoader();

workspaceLoader.initialize();

    }

);