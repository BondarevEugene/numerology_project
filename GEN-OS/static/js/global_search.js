/*
═══════════════════════════════════════════════════════════════════════
Global Search

BUILD:0144
═══════════════════════════════════════════════════════════════════════
*/

class GlobalSearch {

    constructor() {

        this.input =
            document.getElementById(
                "global-search"
            );

        this.initialize();
    }

    initialize() {

        if (!this.input) {

            return;
        }

        this.input.addEventListener(

            "keyup",

            event => {

                const value =
                    event.target.value;

                console.log(
                    "[SEARCH]",
                    value
                );

            }

        );
    }
}

window.addEventListener(

    "DOMContentLoaded",

    () => {

        new GlobalSearch();

    }

);