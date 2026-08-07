/*
═══════════════════════════════════════════════════════════════════════
GENESIS API CLIENT
BUILD 0400
═══════════════════════════════════════════════════════════════════════
*/

class API {
    async get(url) {
        const response =
            await fetch(url);
        if (!response.ok)
            throw new Error(url);
        return await response.json();
    }

    async post(url, data) {
        const response =
            await fetch(
                url,
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/json"
                    },
                    body: JSON.stringify(data)
                }
            );
        if (!response.ok)
            throw new Error(url);
        return await response.json();
    }

    humanProfile() {
        return this.get(
            "/api/human/profile"
        );
    }
    humanWorkspace() {
        return this.get(
            "/api/human/workspace"
        );
    }
    humanDashboard() {
        return this.get(
            "/api/human/dashboard"
        );
    }
    humanStatistics() {
        return this.get(
            "/api/human/statistics"
        );
    }
}
window.api =
    new API();