/*
═══════════════════════════════════════════════════════════════════════
API Client

BUILD:0123
═══════════════════════════════════════════════════════════════════════
*/

class ApiClient {

    async get(url) {

        const response =
            await fetch(url);

        return await response.json();
    }

    async post(
        url,
        payload
    ) {

        const response =
            await fetch(
                url,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            payload
                        )
                }
            );

        return await response.json();
    }
}

window.api =
    new ApiClient();