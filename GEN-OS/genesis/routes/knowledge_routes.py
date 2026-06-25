"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
GEN-OS

Knowledge Workspace Routes

BUILD:0019

Назначение:
Flask-маршруты рабочей области знаний.

UI никогда не работает напрямую с Loader.
UI работает только через API.

═══════════════════════════════════════════════════════════════════════
"""

from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import request

from genesis.api.knowledge_api import KnowledgeAPI

knowledge_bp = Blueprint(
    "knowledge",
    __name__,
    url_prefix="/knowledge"
)
api = KnowledgeAPI()


@knowledge_bp.route("/")
def workspace():
    return render_template(
        "workspace/knowledge_workspace.html"
    )


@knowledge_bp.route("/domains")
def domains():
    return jsonify(
        api.domains()
    )


@knowledge_bp.route("/types/<domain>")
def entity_types(domain):
    return jsonify(
        api.entity_types(
            domain
        )
    )


@knowledge_bp.route("/entities")
def entities():
    domain = request.args.get(
        "domain"
    )
    entity_type = request.args.get(
        "type"
    )
    return jsonify(
        api.entities(
            domain,
            entity_type
        )
    )

@knowledge_bp.route("/entity")
def entity():
    domain = request.args.get(
        "domain"
    )
    entity_type = request.args.get(
        "type"
    )
    entity_id = request.args.get(
        "id"
    )
    return jsonify(
        api.entity(
            domain,
            entity_type,
            entity_id
        )
    )


@knowledge_bp.route(
    "/statistics"
)
def statistics():
    return jsonify(
        api.statistics()
    )


@knowledge_bp.route(
    "/health"
)
def health():
    return jsonify(
        api.health()
    )