/*
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
Base UI Component
BUILD:0200
═══════════════════════════════════════════════════════════════════════
*/

class Component {
    constructor(selector = null) {
        this.selector = selector;
        this.element = selector
            ? document.querySelector(selector)
            : null;
    }
    initialize() {}
    render() {}
    refresh() {}
    destroy() {}
    show() {
        if (this.element) {
            this.element.classList.remove("hidden");
        }
    }
    hide() {
        if (this.element) {
            this.element.classList.add("hidden");
        }
    }
}
