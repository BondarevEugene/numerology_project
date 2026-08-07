/*
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
Status Bar Controller
BUILD 0300
═══════════════════════════════════════════════════════════════════════
*/

class StatusBar {

    constructor() {
        this.initialized = false;
        this.container = null;
        this.workspaceNode = null;
        this.messageNode = null;
        this.stateNode = null;
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
        this.container =
            document.querySelector(".gen-statusbar");
        this.workspaceNode =
            document.querySelector(".gen-status-workspace");
        this.messageNode =
            document.querySelector(".gen-status-message");
        this.stateNode =
            document.querySelector(".gen-status-state");
        console.log("[StatusBar] Ready");
        this.setState("READY");
        this.setMessage("System initialized");

    }

    /*
    ==========================================================
    WORKSPACE
    ==========================================================
    */

    setWorkspace(name) {
        if (!this.workspaceNode)
            return;
        this.workspaceNode.textContent = name;
    }
    /*
    ==========================================================
    MESSAGE
    ==========================================================
    */

    setMessage(text) {
        if (!this.messageNode)
            return;
        this.messageNode.textContent = text;
    }

    /*
    ==========================================================
    STATE
    ==========================================================
    */

    setState(text) {
        if (!this.stateNode)
            return;
        this.stateNode.textContent = text;
    }

    /*
    ==========================================================
    LOG
    ==========================================================
    */

    info(message) {
        this.setMessage(message);
    }
    success(message) {
        this.setState("READY");
        this.setMessage(message);
    }
    warning(message) {
        this.setState("WARNING");
        this.setMessage(message);
    }
    error(message) {
        this.setState("ERROR");
        this.setMessage(message);
    }
}

/*
==========================================================
GLOBAL
==========================================================
*/

window.statusbar = new StatusBar();