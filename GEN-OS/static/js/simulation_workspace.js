class SimulationWorkspace {
constructor() {
this.initialize();
}
initialize() {
console.log(
"[GEN-OS] Simulation Workspace Ready"
);
}
runSimulation() {
console.log(
"[GEN-OS] Simulation Started"
);
}
}
window.addEventListener(
"DOMContentLoaded",
() => {
new SimulationWorkspace();
}
);