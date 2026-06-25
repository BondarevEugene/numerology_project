/*
═══════════════════════════════════════════════════════════════════════
Inspector

BUILD:0118
═══════════════════════════════════════════════════════════════════════
*/

class Inspector {

    show(entity) {

        console.log(
            "[INSPECTOR]",
            entity
        );
    }

    clear() {

        console.log(
            "[INSPECTOR] clear"
        );
    }
}

window.inspector =
    new Inspector();