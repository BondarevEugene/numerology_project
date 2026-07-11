/*
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
Explorer
BUILD 0300
═══════════════════════════════════════════════════════════════════════
*/

class Explorer {
    constructor() {
        this.root = null;
    }

    /*
    =====================================================
    INIT
    =====================================================
    */

    initialize() {
        this.root = document.querySelector(".shell-explorer");
        if (!this.root) {
            console.warn(
                "[Explorer] shell-explorer not found."
            );
            return;
        }
        this.bind();
        console.log(
            "[Explorer] Ready"
        );
    }

    /*
    =====================================================
    EVENTS
    =====================================================
    */

    bind() {
        this.root.addEventListener(
            "click",
            e => {
                const item =
                    e.target.closest(
                        "[data-workspace]"
                    );
                if (!item)
                    return;
                const workspace =
                    item.dataset.workspace;

                if (!workspace)
                    return;

                console.log(
                    "[Explorer]",
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
        );
    }
}

window.explorer = new Explorer();