/*
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
Human Workspace
BUILD:0113
═══════════════════════════════════════════════════════════════════════
*/

class HumanWorkspace {
    constructor() {
        this.profile = null;
        this.initialize();
    }

    initialize() {
        console.log(
            "[GEN-OS] Human Workspace Ready"
        );

        this.loadProfile();
    }

    loadProfile() {
        console.log(
            "[GEN-OS] Loading Human Profile..."
        );
    }

    refresh() {

        console.log(
            "[GEN-OS] Refresh Profile"
        );
    }
}

window.addEventListener(
    "DOMContentLoaded",
    () => {
        new HumanWorkspace();
    }
);