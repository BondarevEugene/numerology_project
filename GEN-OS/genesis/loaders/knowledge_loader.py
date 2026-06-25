"""
═══════════════════════════════════════════════════════════════════════════════
GENESIS HR® Enterprise
GEN-OS Platform
═══════════════════════════════════════════════════════════════════════════════

BUILD:0018
FILE:knowledge_loader.py
LOCATION:GEN-OS/genesis/loaders/
LAYER:Knowledge Storage Layer
PURPOSE:Loads and saves all Knowledge Packages.

KnowledgeLoader is the only module allowed
to directly access the filesystem.

Supported formats:
• JSON
• Registry Packages
• Future:
    - Excel
    - CSV
    - ESCO
    - O*NET
    - REST Providers
═══════════════════════════════════════════════════════════════════════════════
"""

import json
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional


class KnowledgeLoader:

    def __init__(self):

        self.root = (
            Path(__file__)
            .resolve()
            .parent.parent
            / "genesis_knowledge"
            / "domains"
        )

    # =====================================================
    # DOMAINS
    # =====================================================

    def available_domains(self) -> List[str]:
        if not self.root.exists():
            return []
        return sorted(
            [
                p.name
                for p in self.root.iterdir()
                if p.is_dir()
            ]
        )
    # =====================================================
    # ENTITY TYPES
    # =====================================================

    def entity_types(
        self,
        domain: str
    ) -> List[str]:
        domain_path = self.root / domain
        if not domain_path.exists():
            return []
        folders = []
        for item in domain_path.iterdir():
            if item.is_dir():
                folders.append(
                    item.name
                )
        return sorted(
            folders
        )

    # =====================================================
    # LIST
    # =====================================================

    def load_entities(
        self,
        domain: str,
        entity_type: str
    ) -> List[Dict]:
        folder = (
            self.root
            / domain
            / entity_type
        )
        if not folder.exists():
            return []
        entities = []
        for file in folder.glob("*.json"):
            with open(
                file,
                encoding="utf-8"
            ) as fp:
                entities.append(
                    json.load(fp)
                )
        return entities

    # =====================================================
    # LOAD SINGLE
    # =====================================================

    def load_entity(
        self,
        domain: str,
        entity_type: str,
        entity_id: str
    ) -> Optional[Dict]:
        file = (
            self.root
            / domain
            / entity_type
            / f"{entity_id}.json"
        )
        if not file.exists():
            return None
        with open(
            file,
            encoding="utf-8"
        ) as fp:
            return json.load(
                fp
            )

    # =====================================================
    # SAVE
    # =====================================================

    def save_entity(
        self,
        domain: str,
        entity_type: str,
        entity: Dict
    ) -> bool:
        folder = (
            self.root
            / domain
            / entity_type
        )
        folder.mkdir(
            parents=True,
            exist_ok=True
        )
        file = (
            folder
            / f"{entity['id']}.json"
        )
        with open(
            file,
            "w",
            encoding="utf-8"
        ) as fp:
            json.dump(
                entity,
                fp,
                indent=4,
                ensure_ascii=False
            )
        return True

    # =====================================================
    # DELETE
    # =====================================================

    def delete_entity(
        self,
        domain: str,
        entity_type: str,
        entity_id: str
    ) -> bool:
        file = (
            self.root
            / domain
            / entity_type
            / f"{entity_id}.json"
        )
        if not file.exists():
            return False
        file.unlink()
        return True

    # =====================================================
    # EXISTS
    # =====================================================

    def exists(
        self,
        domain: str,
        entity_type: str,
        entity_id: str

    ) -> bool:

        file = (

            self.root
            / domain
            / entity_type
            / f"{entity_id}.json"
        )
        return file.exists()

    # =====================================================
    # CREATE FOLDER
    # =====================================================

    def create_domain(
        self,
        domain: str
    ):
        (
            self.root
            / domain
        ).mkdir(
            parents=True,
            exist_ok=True
        )

    # =====================================================
    # INFO
    # =====================================================

    def health(self):
        return {
            "loader": "KnowledgeLoader",
            "root": str(self.root),
            "domains": len(
                self.available_domains()
            )
        }