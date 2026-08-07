/*
====================================================
GENESIS APPLICATION
====================================================
*/

window.addEventListener("DOMContentLoaded", () => {

    console.log("[APP] Booting...");

    if (!window.Genesis) {
        console.error("Genesis Kernel not found.");
        return;
    }

    window.Genesis.boot();

    if (window.diagnostics) {
        window.diagnostics.check();
    }

    console.log("[APP] Ready.");

});