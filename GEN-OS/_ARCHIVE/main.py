"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   GENESIS HR® / GEN-OS                                                      ║
║──────────────────────────────────────────────────────────────────────────────║
║ MODULE      : Web Bootstrap                                                 ║
║ FILE        : api/main.py                                                   ║
║ LAYER       : Application                                                   ║
║ PURPOSE     : Flask application bootstrap and API routes                    ║
║ BUILD       : 0200                                                          ║
║ STATUS      : ACTIVE                                                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from pathlib import Path
import sys

# =============================================================================
# PROJECT ROOT
# =============================================================================

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

BASE_DIR = ROOT

# =============================================================================
# FLASK
# =============================================================================

from flask import Flask, render_template, abort

# =============================================================================
# PLATFORM
# =============================================================================

from kernel.platform import platform

# =============================================================================
# SERVICES
# =============================================================================

from services.human_service import human_service
from services.knowledge_service import knowledge_service

# =============================================================================
# APPLICATION
# =============================================================================

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)

platform.boot()
# =============================================================================
# Регистрация Blueprint'ов
# =============================================================================

from routes.workspace_routes import workspace_bp
from routes.decision_routes import decision_bp
from routes.import_workspace import import_bp

app.register_blueprint(workspace_bp)
app.register_blueprint(decision_bp)
app.register_blueprint(import_bp)

# =============================================================================
# WEB
# =============================================================================

@app.route("/")
def index():
    return render_template("genos_shell.html")

@app.route("/workspace/<workspace_id>")
def workspace(workspace_id):
    print("=" * 60)
    print("Workspace requested:", workspace_id)

    ws = platform.workspace.get(workspace_id)

    print("Workspace object:", ws)
    print("=" * 60)

    if ws is None:
        return {
            "error": "Workspace not found",
            "workspace": workspace_id
        }, 404

    platform.runtime.switch(workspace_id)

    return platform.workspace.render(workspace_id)


# =============================================================================
# HUMAN API
# =============================================================================

@app.get("/api/human/profile")
def human_profile():
    return human_service.load_profile()


@app.get("/api/human/dashboard")
def human_dashboard():
    return human_service.dashboard()


@app.get("/api/human/workspace")
def human_workspace():
    return human_service.workspace()


@app.get("/api/human/summary")
def human_summary():
    return human_service.summary()


@app.get("/api/human/statistics")
def human_statistics():
    return human_service.statistics()


# =============================================================================
# HEALTH
# =============================================================================

@app.get("/api/health")
def health():
    return {
        "status": "OK",
        "platform": "GEN-OS",
        "build": "0200"
    }


@app.get("/test")
def test():
    return "TEST OK"


@app.get("/api/knowledge/workspace")
def knowledge_workspace():
    return knowledge_service.workspace()


@app.get("/api/knowledge/statistics")
def knowledge_statistics():
    return knowledge_service.statistics()


@app.get("/api/knowledge/summary")
def knowledge_summary():
    return knowledge_service.summary()


@app.get("/api/knowledge/dashboard")
def knowledge_dashboard():
    return knowledge_service.dashboard()


@app.get("/api/knowledge/all")
def knowledge_all():
    return knowledge_service.all()


@app.get("/api/knowledge/node/<node_id>")
def knowledge_node(node_id):
    return knowledge_service.get(node_id)
