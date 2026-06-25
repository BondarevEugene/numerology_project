/*
═══════════════════════════════════════════════════════════════════════
Import Workspace

BUILD:0115
═══════════════════════════════════════════════════════════════════════
*/

class ImportWorkspace {

    constructor() {

        this.file = null;

        this.initialize();
    }

    initialize() {

        console.log(
            "[GEN-OS] Import Workspace Ready"
        );

        this.bindFileInput();
    }

    bindFileInput() {

        const input =
            document.getElementById(
                "import-file"
            );

        if (!input) {

            return;
        }

        input.addEventListener(
            "change",
            event => {

                this.file =
                    event.target.files[0];

                if (!this.file) {

                    return;
                }

                console.log(
                    "[IMPORT]",
                    this.file.name
                );
            }
        );
    }
}

window.addEventListener(
    "DOMContentLoaded",
    () => {

        new ImportWorkspace();
    }
);