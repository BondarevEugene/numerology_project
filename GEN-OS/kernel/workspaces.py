"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   GENESIS HR® / GEN-OS                                                       ║
║──────────────────────────────────────────────────────────────────────────────║
║ MODULE      : Configuration                                                  ║
║ FILE        : kernel/workspaces.py                                           ║
║ LAYER       : Core                                                           ║
║ PURPOSE     : Workspace definitions and registry                             ║
║ BUILD       : 0200                                                           ║
║ STATUS      : ACTIVE                                                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

WORKSPACES = {

    "dashboard": {
        "title": "Genesis Control Center",
        "template": "workspaces/dashboard/dashboard.html",
        "icon": "dashboard"
    },

    "human": {
        "title": "Human Intelligence",
        "template": "workspaces/human/human.html",
        "icon": "person"
    },

    "knowledge": {
        "title": "Knowledge Center",
        "template": "workspaces/knowledge/knowledge.html",
        "icon": "hub"
    },

    "graph": {
        "title": "Relationship Intelligence",
        "template": "workspaces/graph/graph.html",
        "icon": "graph"
    },

    "career": {
        "title": "Career Intelligence",
        "template": "workspaces/career/career.html",
        "icon": "work"
    },

    "simulation": {
        "title": "Simulation Center",
        "template": "workspaces/simulation/simulation.html",
        "icon": "science"
    },

    "platform": {
        "title": "Platform",
        "template": "workspaces/platform/platform.html",
        "icon": "settings"
    },

    "ai": {
        "title": "AI Copilot",
        "template": "workspaces/ai/ai.html",
        "icon": "smart_toy"
    },

    "import": {
        "title": "Knowledge Import",
        "template": "workspaces/import/import.html",
        "icon": "download"
    }

}