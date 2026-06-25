/*
═══════════════════════════════════════════════════════════════════════
Graph Renderer

BUILD:0125
═══════════════════════════════════════════════════════════════════════
*/

class GraphRenderer {

    constructor(
        containerId
    ) {

        this.container =
            document.getElementById(
                containerId
            );
    }

    render(
        graph
    ) {

        if (
            !this.container
        ) {

            return;
        }

        this.container.innerHTML = `

            <div
                style="
                display:flex;
                justify-content:center;
                align-items:center;
                height:100%;
                font-size:24px;">
                Graph Loaded
            </div>

        `;

        console.log(
            "[GRAPH]",
            graph.nodeCount(),
            graph.edgeCount()
        );
    }
}