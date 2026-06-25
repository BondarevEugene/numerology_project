/*
═══════════════════════════════════════════════════════════════════════
Console Engine
BUILD:0120
═══════════════════════════════════════════════════════════════════════
*/

class GenConsole {
    constructor() {
        this.buffer = [];
    }
    info(message) {
        this.write(
            "INFO",
            message
        );
    }

    warning(message) {
        this.write(
            "WARNING",
            message
        );
    }

    error(message) {
        this.write(
            "ERROR",
            message
        );
    }

    write(
        level,
        message
    ) {

        const record = {
            timestamp:
                new Date()
                .toISOString(),

            level,

            message
        };

        this.buffer.push(
            record
        );

        console.log(
            `[${level}]`,
            message
        );

        document.dispatchEvent(
            new CustomEvent(
                "console.message",
                {
                    detail: record
                }
            )
        );
    }

    history() {

        return this.buffer;
    }
}

window.genConsole =
    new GenConsole();