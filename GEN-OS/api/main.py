"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
GEN-OS
WEB Bootstrap
═══════════════════════════════════════════════════════════════════════
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

BASE_DIR = ROOT

from flask import Flask
from flask import render_template
from flask import abort

from kernel.platform import platform
from kernel.workspaces import WORKSPACES

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)

platform.boot()


@app.route("/")
def shell():

    return render_template(
        "shell/shell.html",
        **platform.context()
    )


@app.route("/workspace/<workspace_id>")
def workspace(workspace_id):
    if workspace_id not in WORKSPACES:
        abort(404)
    platform.runtime.switch(workspace_id)
    return render_template(
        "shell/shell.html",
        **platform.context()
    )


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )