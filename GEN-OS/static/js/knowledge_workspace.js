/*
═══════════════════════════════════════════════════════════════════════
Knowledge Workspace
BUILD:0114
═══════════════════════════════════════════════════════════════════════
*/

class KnowledgeWorkspace {
    constructor() {
        this.selectedEntity = null;
        this.initialize();
    }

    initialize() {
        console.log(
            "[GEN-OS] Knowledge Workspace Ready"
        );
        this.bindEvents();
    }
    bindEvents() {
        document
            .querySelectorAll(
                ".knowledge-list li"
            )
            .forEach(
                node => {

                    node.addEventListener(
                        "click",
                        () => {

                            this.selectEntity(
                                node.innerText
                            );
                        }
                    );

                }
            );
    }

    selectEntity(name) {

        this.selectedEntity = name;

        console.log(
            "[ENTITY]",
            name
        );
    }
}

window.addEventListener(
    "DOMContentLoaded",
    () => {

        new KnowledgeWorkspace();
    }
);