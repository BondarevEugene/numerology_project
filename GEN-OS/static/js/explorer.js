/*
═══════════════════════════════════════════════════════════════════════
Explorer

BUILD:0117
═══════════════════════════════════════════════════════════════════════
*/

class Explorer {

    constructor() {

        this.initialize();
    }

    initialize() {

        this.bindTree();
    }

    bindTree() {

        document
            .querySelectorAll(
                ".gen-tree-item"
            )
            .forEach(
                item => {

                    item.addEventListener(
                        "click",
                        () => {

                            document
                                .querySelectorAll(
                                    ".gen-tree-item"
                                )
                                .forEach(
                                    x => x.classList.remove(
                                        "active"
                                    )
                                );

                            item.classList.add(
                                "active"
                            );

                            console.log(
                                item.dataset.workspace
                            );
                        }
                    );

                }
            );
    }
}

window.addEventListener(
    "DOMContentLoaded",
    () => {

        new Explorer();
    }
);