class PlatformWorkspace {
    constructor() {
        console.log(
            "[GEN-OS] Platform Workspace Ready"
        );
    }
}

window.addEventListener(
    "DOMContentLoaded",
    () => {
        new PlatformWorkspace();
    }
);