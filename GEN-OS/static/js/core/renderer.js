/*
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
Base Renderer
BUILD:0200
═══════════════════════════════════════════════════════════════════════
*/

class Renderer {
    constructor(container = null) {
        this.container = container
            ? document.querySelector(container)
            : null;
    }
    render(data) {}
    clear() {
        if (this.container) {
            this.container.innerHTML = "";
        }
    }
    update(data) {
        this.render(data);
    }
}
