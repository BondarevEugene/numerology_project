/*
═══════════════════════════════════════════════════════════════════════
Graph Engine

BUILD:0124
═══════════════════════════════════════════════════════════════════════
*/

class GraphEngine {

    constructor() {

        this.nodes = [];

        this.edges = [];
    }

    load(
        nodes,
        edges
    ) {

        this.nodes =
            nodes || [];

        this.edges =
            edges || [];
    }

    nodeCount() {

        return this.nodes.length;
    }

    edgeCount() {

        return this.edges.length;
    }

    clear() {

        this.nodes = [];

        this.edges = [];
    }
}

window.graphEngine =
    new GraphEngine();