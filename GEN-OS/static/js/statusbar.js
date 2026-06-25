/*
═══════════════════════════════════════════════════════════════════════
Status Bar

BUILD:0121
═══════════════════════════════════════════════════════════════════════
*/

class StatusBar {

    constructor() {

        this.status =
            "READY";
    }

    setStatus(
        status
    ) {

        this.status =
            status;

        console.log(
            "[STATUS]",
            status
        );
    }

    getStatus() {

        return this.status;
    }
}

window.statusBar =
    new StatusBar();