/*
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
Base Service
BUILD:0200
═══════════════════════════════════════════════════════════════════════
*/
class Service {
    constructor() {
        this.api = window.api;
    }
    async get(url) {
        return this.api.get(url);
    }
    async post(url, data) {
        return this.api.post(url, data);
    }
}
