/*
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
Human Workspace
BUILD:0113
═══════════════════════════════════════════════════════════════════════
*/

class HumanWorkspace {
    constructor() {

        this.profile = null;
        this.workspace = null;
        this.dashboard = [];
        this.loading = false;

        this.initialize();

    }

    async initialize() {

        console.log("[GEN-OS] Human Workspace Ready");

        await this.loadWorkspace();

    }

    async loadWorkspace() {

        try {
            this.loading = true;
            const response = await fetch(
                "/api/human/workspace"
            );
            if (!response.ok)
                throw new Error("Workspace loading failed");
            this.workspace = await response.json();
            this.profile = this.workspace.profile;
            this.dashboard = this.workspace.dashboard;
            this.render();
        }
        catch(error){
            console.error(error);
        }
        finally{
            this.loading = false;
        }
    }

    async refresh(){
            await this.loadWorkspace();
        }

window.addEventListener(
    "DOMContentLoaded",
    () => {
        new HumanWorkspace();
    }
);

    render(){
    this.renderProfile();
    this.renderDashboard();
    this.renderCompetencies();
    this.renderProfessions();
    this.renderRisks();
    this.renderRoadmap();
}
    renderProfile(){}
    renderDashboard(){}
    renderCompetencies(){}
    renderProfessions(){}
    renderRisks(){}
    renderRoadmap(){}