/*
══════════════════════════════════════════════════════════════════════

GENESIS HR®

Workspace Manager

BUILD 0500

══════════════════════════════════════════════════════════════════════
*/

class WorkspaceManager {

    constructor() {

        this.current = "dashboard";

        this.host = document.querySelector(".workspace-body");

        this.title = document.querySelector(".workspace-title h2");

        this.subtitle = document.querySelector(".workspace-title span");

        this.routes = {

            dashboard: "/workspace/dashboard",

            human: "/workspace/human",

            knowledge: "/workspace/knowledge",

            graph: "/workspace/graph",

            career: "/workspace/career",

            platform: "/workspace/platform"

        };

        this.titles = {

            dashboard: {
                title: "Dashboard",
                subtitle: "System Overview"
            },

            human: {
                title: "Digital Twin",
                subtitle: "Human Intelligence Workspace"
            },

            knowledge: {
                title: "Knowledge Registry",
                subtitle: "Knowledge Graph"
            },

            graph: {
                title: "Knowledge Graph",
                subtitle: "Graph Engine"
            },

            career: {
                title: "Career Intelligence",
                subtitle: "Professional Analytics"
            },

            platform: {
                title: "Platform",
                subtitle: "Kernel Configuration"
            }

        };

    }

    async load(name) {

        if (!this.routes[name]) {

            console.error("Unknown workspace:", name);

            return;

        }

        try {

            this.setLoading();

            const response = await fetch(this.routes[name]);

            if (!response.ok) {

                throw new Error(response.status);

            }

            const html = await response.text();

            this.host.innerHTML = html;

            this.current = name;

            this.updateHeader(name);

            this.activateDock(name);

            this.activateExplorer(name);

            this.log("Workspace", name + " loaded");

        }

        catch (e) {

            console.error(e);

            this.host.innerHTML = `

                <div class="gen-card">

                    <h2>Workspace loading failed</h2>

                    <p>${e}</p>

                </div>

            `;

        }

    }

    setLoading() {

        this.host.innerHTML = `

            <div class="gen-card">

                <h2>Loading...</h2>

            </div>

        `;

    }

    updateHeader(name) {

        if (!this.titles[name]) return;

        this.title.textContent =

            this.titles[name].title;

        this.subtitle.textContent =

            this.titles[name].subtitle;

    }

    activateDock(name) {

        document

            .querySelectorAll(".dock-button")

            .forEach(button => {

                button.classList.remove("active");

            });

        const button =

            document.querySelector(

                '.dock-button[data-workspace="' +

                name +

                '"]'

            );

        if (button)

            button.classList.add("active");

    }

    activateExplorer(name) {

        document

            .querySelectorAll(".tree-item")

            .forEach(item => {

                item.classList.remove("active");

            });

        const item =

            document.querySelector(

                '.tree-item[data-workspace="' +

                name +

                '"]'

            );

        if (item)

            item.classList.add("active");

    }

    log(title, text) {

        const body =

            document.querySelector(".console-body");

        if (!body) return;

        const row =

            document.createElement("div");

        row.className = "console-line";

        const time =

            new Date()

            .toLocaleTimeString();

        row.innerHTML =

            `<div class="console-time">${time}</div>

             <div>

                <span class="console-success">

                    ${title}

                </span>

                ${text}

             </div>`;

        body.appendChild(row);

        body.scrollTop = body.scrollHeight;

    }

}

window.Workspace = new WorkspaceManager();

window.loadWorkspace = function(name){

    window.Workspace.load(name);

};

window.addEventListener(

    "DOMContentLoaded",

    () => {

        document

            .querySelectorAll(".dock-button")

            .forEach(button => {

                button.onclick = () =>

                    loadWorkspace(

                        button.dataset.workspace

                    );

            });

        document

            .querySelectorAll(".tree-item")

            .forEach(item => {

                item.onclick = () =>

                    loadWorkspace(

                        item.dataset.workspace

                    );

            });

    }

);