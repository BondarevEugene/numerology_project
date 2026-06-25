class GraphWorkspace {
constructor() {
this.selectedNode = null;
this.initialize();
}
initialize() {
console.log(
"[GEN-OS] Graph Workspace Ready"
);
this.bindEvents();
}
bindEvents() {
document
.querySelectorAll(
".graph-result-item"
)
.forEach(
item => {
item.addEventListener(
"click",
() => {
this.selectNode(
item.innerText
);
}
);
}
);
}
selectNode(name) {
this.selectedNode = name;
console.log(
"[GRAPH]",
name
);
}
}
window.addEventListener(
"DOMContentLoaded",
() => {
new GraphWorkspace();
}
);