/*
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
Console Controller
BUILD 0300
══════════════════════════════════════════════════════════════════════
*/

class GenesisConsole {
    constructor() {
        this.container = null;
        this.initialized = false;
        this.maxLines = 500;
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
        this.container = document.querySelector(
            ".gen-console-body"
        );
        console.log(
            "[Console] Ready"
        );
        this.write(
            "GENESIS Console initialized."
        );
    }

    /*
    ==========================================================
    WRITE
    ==========================================================
    */

    write(message, level = "info") {
        if (!this.container)
            return;
        const row =
            document.createElement("div");
        row.className =
            "gen-console-row " + level;
        const time =
            new Date().toLocaleTimeString();
        row.innerHTML =
            `<span class="console-time">${time}</span>
             <span class="console-text">${message}</span>`;
        this.container.appendChild(row);
        while (
            this.container.children.length >
            this.maxLines
        ) {
            this.container.removeChild(
                this.container.firstChild
            );
        }
        this.container.scrollTop =
            this.container.scrollHeight;
    }

    /*
    ==========================================================
    CLEAR
    ==========================================================
    */

    clear() {
        if (!this.container)
            return;
        this.container.innerHTML = "";
    }

    /*
    ==========================================================
    LEVELS
    ==========================================================
    */

    info(text) {
        this.write(text, "info");
    }
    success(text) {
        this.write(text, "success");
    }
    warning(text) {
        this.write(text, "warning");
    }
    error(text) {
        this.write(text, "error");
    }
}

/*
==========================================================
GLOBAL
==========================================================
*/

window.genConsole =
    new GenesisConsole();