/*
═══════════════════════════════════════════════════════════════════════
 GENESIS HR®
 Frontend Kernel
 BUILD 0201
═══════════════════════════════════════════════════════════════════════
*/

class GenesisKernel {
    constructor() {
        this.version = "2.1";
        this.registry = new Registry();
        this.state = new StateManager();
        this.bus = null;
        this.booted = false;
    }

    /*
    ===============================================================
    BOOT
    ===============================================================
    */

    boot() {
        if (this.booted) {
            console.warn("[Genesis] Kernel already booted.");
            return;
        }

        console.group("GENESIS KERNEL");
        this.bus = window.bus || null;
        this.registerModules();
        this.bindEvents();
        this.restoreSession();
        this.bootUI();
        this.booted = true;
        this.log("Kernel Ready");
        console.groupEnd();
        this.emit("kernel.ready");
         }

    /*
===============================================================
REGISTRY
===============================================================
*/

register(name, module) {
    if (!module) {
        return;
    }
    this.registry.register(name, module);}
get(name) {return this.registry.get(name);}
has(name) {return this.registry.has(name);}

modules() {
    return this.registry.list();}

/*
===============================================================
UI
===============================================================
*/

bootUI() {
    this.modules().forEach(name => {
        const module = this.get(name);
        if (!module)
            return;
        if (typeof module.initialize === "function") {
            module.initialize();
        }
    });
}


    /*
    ===============================================================
    MODULE REGISTRATION
    ===============================================================
    */

    registerModules() {
        const modules = {
            bus: window.bus,
            api: window.api,
            toolbar: window.toolbar,
            explorer: window.explorer,
            workspaceLoader: window.workspaceLoader,
            inspector: window.inspector,
            statusbar: window.statusbar,
            console: window.genConsole,
            graphEngine: window.graphEngine,
            graphRenderer: window.graphRenderer,
            shell: window.shell
        };

        Object.entries(modules).forEach(
            ([name, module]) => {
                if (module) {
                    this.register(name, module);
                }
            }
        );

        this.log(
            "Modules:",
            this.modules().length
        );
        }
    /*
    ===============================================================
    EVENTS
    ===============================================================
    */

    bindEvents() {
        if (!this.bus) {
            console.warn(
                "EventBus not found."
            );
            return;
        }

    this.bus.on(
        "workspace.change",
        payload => {
            this.changeWorkspace(
                payload.workspace
            );
        }
    );

    this.bus.on(
        "toolbar.action",
        payload => {
            this.executeToolbar(
                payload.action
            );
        }
    );
    }
    emit(event, payload = {}) {
        if (!this.bus) return;
        this.bus.emit(event, payload);
    }

    /*
    ===============================================================
    WORKSPACES
    ===============================================================
    */

    changeWorkspace(id) {
        this.state.set(
            "workspace",
            id
        );

        const loader =
            this.get(
                "workspaceLoader"
            );
        if (!loader) {
            console.warn(
                "WorkspaceLoader missing."
            );
            return;
        }
        if (typeof loader.open === "function") {
            loader.open(id);
        }
        else if (
            typeof loader.load ===
            "function"
        ) {
            loader.load(id);
        }
    }

    /*
    ===============================================================
    TOOLBAR
    ===============================================================
    */

    executeToolbar(action) {
        switch (action) {
            case "toggleExplorer":
                this.toggle(
                    ".shell-explorer"
                );
                break;
            case "toggleInspector":
                this.toggle(
                    ".shell-inspector"
                );
                break;
            case "toggleConsole":
                this.toggle(
                    ".shell-console"
                );
                break;
            default:
                this.log(
                    "Toolbar:",
                    action
                );
        }
    }

    /*
    ===============================================================
    UI
    ===============================================================
    */

    toggle(selector) {
        const node =
            document.querySelector(selector);
        if (!node) return;
        node.classList.toggle("hidden");
    }


    /*
    ===============================================================
    SESSION
    ===============================================================
    */

    restoreSession() {
        const state =
            localStorage.getItem(
                "genesis-state"
            );
        if (!state) return;
        try {
            this.state.restore(
                JSON.parse(state)
            );
        }
        catch (e) {
            console.warn(e);
        }
    }
    saveSession() {
        localStorage.setItem(
            "genesis-state",
            JSON.stringify(
                this.state.snapshot()
            )
        );
    }
    /*
    ===============================================================
    DIAGNOSTICS
    ===============================================================
    */

    ready() {
        return this.booted;
    }
    shutdown() {
        this.saveSession();
        this.booted = false;
    }

    log(...args) {
        console.log(
            "[Genesis]",
            ...args
        );
    }

}

/*
==============================================================
GLOBAL
==============================================================
*/

window.Genesis = new GenesisKernel();
window.kernel = window.Genesis;

diagnostics(){
    return{
        version:this.version,
        modules:this.modules(),
        state:this.state.snapshot(),
        booted:this.booted
    };
}

runtime(){
    return{
        workspace:
            this.state.get(
                "workspace"
            ),
        online:
            this.state.get(
                "online"
            ),
        loading:
            this.state.get(
                "loading"
            )
    };
}
