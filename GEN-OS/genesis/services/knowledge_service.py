"""
═══════════════════════════════════════════════════════════════════════════════
GENESIS HR® Enterprise
GEN-OS Platform
═══════════════════════════════════════════════════════════════════════════════
BUILD:0018

FILE:knowledge_service.py

LOCATION:GEN-OS/genesis/services/

LAYER:Business Service Layer

PURPOSE:Central business logic of Knowledge Workspace.

This service is responsible for:

• loading entities
• saving entities
• creating entities
• deleting entities
• updating metadata
• searching entities
• listing domains
• listing entity types
• delegating all IO operations to KnowledgeLoader

The service DOES NOT know anything about:

• Flask
• HTML
• JavaScript
• Registry implementation
• Storage implementation

Dependencies:knowledge_loader.py
═══════════════════════════════════════════════════════════════════════════════
"""

from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional

from genesis.loaders.knowledge_loader import KnowledgeLoader


class KnowledgeService:
    """
    Main business layer of Genesis Knowledge Engine.
    """

    def __init__(self):
        self.loader = KnowledgeLoader()

    # =======================================================
    # DOMAINS
    # =======================================================

    def get_domains(self) -> List[str]:
        return self.loader.available_domains()

    # =======================================================
    # ENTITY TYPES
    # =======================================================

    def get_entity_types(
        self,
        domain: str
    ) -> List[str]:
        return self.loader.entity_types(domain)

    # =======================================================
    # ENTITIES
    # =======================================================

    def list_entities(
        self,
        domain: str,
        entity_type: str
    ) -> List[Dict]:
        return self.loader.load_entities(
            domain,
            entity_type
        )

    def load_entity(
        self,
        domain: str,
        entity_type: str,
        entity_id: str
    ) -> Optional[Dict]:

        return self.loader.load_entity(
            domain,
            entity_type,
            entity_id
        )

    # =======================================================
    # SAVE
    # =======================================================

    def save_entity(
        self,
        domain: str,
        entity_type: str,
        entity: Dict
    ) -> bool:

        return self.loader.save_entity(
            domain,
            entity_type,
            entity
        )

    # =======================================================
    # CREATE
    # =======================================================

    def create_entity(
        self,
        domain: str,
        entity_type: str,
        entity_id: str,
        title: str
    ) -> Dict:

        entity = {
            "id": entity_id,
            "title": title,
            "description": "",
            "tags": [],
            "metadata": {},
            "enabled": True
        }

        self.save_entity(
            domain,
            entity_type,
            entity
        )
        return entity

    # =======================================================
    # DELETE
    # =======================================================

    def delete_entity(
        self,
        domain: str,
        entity_type: str,
        entity_id: str
    ) -> bool:

        return self.loader.delete_entity(
            domain,
            entity_type,
            entity_id
        )

    # =======================================================
    # SEARCH
    # =======================================================

    def search(
        self,
        text: str
    ) -> List[Dict]:
        text = text.lower()
        results = []
        for domain in self.get_domains():
            for entity_type in self.get_entity_types(domain):
                entities = self.list_entities(
                    domain,
                    entity_type
                )
                for entity in entities:
                    title = entity.get(
                        "title",
                        ""
                    ).lower()
                    if text in title:
                        results.append(
                            entity
                        )
        return results

    # =======================================================
    # STATISTICS
    # =======================================================

    def statistics(self):
        total = 0
        domains = {}
        for domain in self.get_domains():
            count = 0
            for entity_type in self.get_entity_types(domain):
                entities = self.list_entities(
                    domain,
                    entity_type
                )
                count += len(
                    entities
                )
            domains[domain] = count
            total += count
        return {
            "total_entities": total,
            "domains": domains
        }
    # =======================================================
    # HEALTH
    # =======================================================

    def health(self):
        return {
            "service": "KnowledgeService",
            "status": "OK",
            "loader": self.loader.__class__.__name__
        }
