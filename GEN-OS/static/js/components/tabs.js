class Tabs {

    constructor(root) {

        this.root = root;
        this.tabs = [];

    }

    initialize() {

        this.tabs = Array.from(
            this.root.querySelectorAll(".gen-tab")
        );

        this.tabs.forEach(tab => {

            tab.addEventListener(
                "click",
                () => this.activate(tab)
            );

        });

    }

    activate(tab) {

        this.tabs.forEach(
            t => t.classList.remove("active")
        );

        tab.classList.add("active");

        const id = tab.dataset.workspace;

        if (window.bus) {

            window.bus.emit(
                "workspace.change",
                {
                    workspace: id
                }
            );

        }

    }

}

window.Tabs = Tabs;