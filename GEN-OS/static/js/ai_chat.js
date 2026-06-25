/*
═══════════════════════════════════════════════════════════════════════
AI Chat

BUILD:0133
═══════════════════════════════════════════════════════════════════════
*/

class AIChat {

    constructor() {

        console.log(
            "[AI] Ready"
        );
    }

    send(
        prompt
    ) {

        console.log(
            "[AI ASK]",
            prompt
        );
    }
}

window.aiChat =
    new AIChat();