"""
═══════════════════════════════════════════════════════════════════════════════
GENESIS HR® Enterprise
GEN-OS Platform
═══════════════════════════════════════════════════════════════════════════════
BUILD:0018

FILE:knowledge_api.py

LOCATION:GEN-OS/genesis/api/

LAYER:Application API Layer

PURPOSE:Public API of Knowledge Workspace.
This module is a thin wrapper above
KnowledgeService.

UI communicates ONLY with this layer.

═══════════════════════════════════════════════════════════════════════════════
"""

from typing import Dict
from typing import List
from typing import Optional

from genesis.services.knowledge_service import KnowledgeService


class KnowledgeAPI:
    def __init__(self):
        self.service = KnowledgeService()

    # ==========================================================
    # DOMAINS
    # ==========================================================
    def domains(self):
        return self.service.get_domains()

    # ==========================================================
    # ENTITY TYPES
    # ==========================================================
    def entity_types(
        self,
        domain: str
    ):
        return self.service.get_entity_types(
            domain
        )

    # ==========================================================
    # ENTITIES
    # ==========================================================

    def entities(
        self,
        domain: str,
        entity_type: str
    ):
        return self.service.list_entities(
            domain,
            entity_type
        )

    # ==========================================================
    # ENTITY
    # ==========================================================

    def entity(
        self,
        domain: str,
        entity_type: str,
        entity_id: str
    ) -> Optional[Dict]:
        return self.service.load_entity(
            domain,
            entity_type,
            entity_id
        )

    # ==========================================================
    # SAVE
    # ==========================================================

    def save(
        self,
        domain: str,
        entity_type: str,
        entity: Dict
    ) -> bool:
        return self.service.save_entity(
            domain,
            entity_type,
            entity
        )

    # ==========================================================
    # CREATE
    # ==========================================================

    def create(
        self,
        domain: str,
        entity_type: str,
        entity_id: str,
        title: str
    ):
        return self.service.create_entity(
            domain,
            entity_type,
            entity_id,
            title
        )

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete(
        self,
        domain: str,
        entity_type: str,
        entity_id: str
    ):
        return self.service.delete_entity(
            domain,
            entity_type,
            entity_id
        )

    # ==========================================================
    # SEARCH
    # ==========================================================

    def search(
        self,
        text: str
    ) -> List[Dict]:
        return self.service.search(
            text
        )

    # ==========================================================
    # STATS
    # ==========================================================

    def statistics(self):
        return self.service.statistics()

    # ==========================================================
    # HEALTH
    # ==========================================================

    def health(self):
        return self.service.health()