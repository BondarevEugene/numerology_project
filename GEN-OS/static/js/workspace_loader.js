/*
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██████╗ ███████╗███╗   ██╗      ██████╗ ███████╗                           ║
║  ██╔════╝ ██╔════╝████╗  ██║     ██╔═══██╗██╔════╝                           ║
║  ██║  ███╗█████╗  ██╔██╗ ██║     ██║   ██║███████╗                           ║
║  ██║   ██║██╔══╝  ██║╚██╗██║     ██║   ██║╚════██║                           ║
║  ╚██████╔╝███████╗██║ ╚████║     ╚██████╔╝███████║                           ║
║   ╚═════╝ ╚══════╝╚═╝  ╚═══╝      ╚═════╝ ╚══════╝                           ║
║                                                                              ║
║──────────────────────────────────────────────────────────────────────────────║
║ MODULE      : Workspace Loader                                               ║
║ FILE        : static/js/workspace_loader.js                                  ║
║ LAYER       : UI Framework                                                   ║
║ PURPOSE     : Workspace Router & Registry                                    ║
║ BUILD       : 0400                                                           ║
║ STATUS      : ACTIVE                                                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
*/

class WorkspaceLoader {

    constructor() {
        this.current = null;
        this.loading = false;
        this.initialized = false;
        this.registry = {};
    }

    /* ========================================================= */

    initialize() {
        if (this.initialized)
            return;
        this.initialized = true;
        console.info(
            "[WorkspaceLoader] Initialized"
        );
    }

    /* ========================================================= */

    register(id, workspace) {
        this.registry[id] = workspace;
    }

    /* ========================================================= */

    get(id) {
        return this.registry[id];
    }

    /* ========================================================= */

    currentWorkspace() {
        return this.current;
    }

    /* ========================================================= */

    isLoading() {
        return this.loading;
    }

    /* ========================================================= */

    async open(id) {
        if (!id)
            return;
        if (this.loading)
            return;
        if (this.current === id)
            return;
        this.loading = true;
        this.current = id;
        console.group("[Workspace]");
        console.log("Opening:", id);
        console.groupEnd();
        if (window.Genesis?.state) {
            window.Genesis.state.set(
                "workspace",
                id
            );
        }

        /*
        -------------------------------------------------------

        BUILD 0400

        Пока используется переход
        между страницами.

        BUILD 0500

        Будет AJAX загрузка.

        -------------------------------------------------------
        */

        window.location.href =
            "/workspace/" + id;
    }

    /* ========================================================= */

    reload() {
        this.loading = false;
        window.location.reload();
    }
}

/* ========================================================= */

window.workspaceLoader =
    new WorkspaceLoader();
