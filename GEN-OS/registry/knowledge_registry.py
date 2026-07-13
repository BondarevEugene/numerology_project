"""
════════════════════════════════════════════════════════════════════════════════════

 GENESIS HR® // OMNIFACTORY EVO
 GEN-OS Platform
 MODULE:     Knowledge Registry
 FILE:     knowledge_registry.py
 BUILD:     0301
 DESCRIPTION
 -----------------------------------------------------------------------------
 Central registry of every domain entity inside GEN-OS.
 The Knowledge Registry is the Single Source of Truth (SSOT)
 for every entity imported from external providers.
 Every Occupation, Skill, Knowledge, Ability, Technology,
 Tool, Task, Education object MUST be registered here before
 becoming part of the Knowledge Graph.

 External providers:

     • O*NET
     • ESCO
     • ASPECTT
     • CareerOneStop
     • Custom Datasets
     • Future AI Providers

 Responsibilities

     • Register entities
     • Track provenance
     • Version entities
     • Resolve aliases
     • Merge duplicates
     • Provide graph-ready objects
     • Audit every modification

 IMPORTANT
     Registry DOES NOT build graphs.
     Registry DOES NOT calculate recommendations.
     Registry DOES NOT import files.
     Registry stores canonical entities only.
════════════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import uuid

from typing import Callable
from typing import Any

import logging
LOGGER = logging.getLogger("GEN-OS.Registry")


# =============================================================================
# REGISTRY ENTITY
# =============================================================================


@dataclass(slots=True)
class RegistryEntity:
    """
    Canonical entity stored inside Knowledge Registry.
    """
    uid: str
    entity_type: str
    name: str
    description: str = ""
    aliases: set[str] = field(default_factory=set)
    external_ids: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    sources: set[str] = field(default_factory=set)
    version: int = 1
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # =============================================================================
    # KNOWLEDGE REGISTRY
    # =============================================================================


class KnowledgeRegistry:
    """
    Central entity registry.
    """
    def __init__(self):
        #
        # uid -> entity
        #
        self._entities: dict[str, RegistryEntity] = {}
        #
        # entity_type
        #
        self._by_type: dict[str, set[str]] = defaultdict(set)
        #
        # normalized_name
        #
        self._by_name: dict[str, str] = {}
        #
        # provider:id
        #
        self._external_index: dict[str, str] = {}
        #
        # aliases
        #
        self._alias_index: dict[str, str] = {}
        #
        # audit
        #
        self._history: list[dict] = []

        # =====================================================
        # EVENT SUBSCRIBERS
        # =====================================================

        self._listeners: list[Callable[..., Any]] = []

    # =============================================================================
    # NORMALIZATION
    # =============================================================================

    @staticmethod
    def normalize_name(name: str) -> str:
        """
        Creates canonical key used inside registry.
        Example:
            Python
            python
            PYTHON
            Python®
        →

            python
        """
        if not name:
            return ""

        normalized = (
            name
            .strip()
            .lower()
            .replace("®", "")
            .replace("™", "")
            .replace("-", " ")
            .replace("_", " ")
        )
        normalized = " ".join(normalized.split())
        return normalized

    # -------------------------------------------------------------------------

    @staticmethod
    def make_external_key(
            provider: str,
            external_id: str
    ) -> str:

        return f"{provider}:{external_id}"

    # -------------------------------------------------------------------------

    @staticmethod
    def new_uid() -> str:
        """
        Generates internal immutable Registry ID.
        """
        return str(uuid.uuid4())

    # ============================================================
    # OBSERVERS
    # ============================================================

    def subscribe(
            self,
            callback: Callable[..., Any]
    ) -> None:
        """
        Subscribe for registry updates.
        """

        if callback not in self._listeners:
            self._listeners.append(callback)

    # ------------------------------------------------------------

    def unsubscribe(
            self,
            callback: Callable[..., Any]
    ) -> None:
        """
        Remove subscriber.
        """

        if callback in self._listeners:
            self._listeners.remove(callback)

    # ------------------------------------------------------------

    def notify(
            self,
            event: str,
            entity=None
    ) -> None:
        """
        Notify subscribers.
        """

        for callback in self._listeners:

            try:

                callback(

                    event=event,

                    entity=entity,

                    registry=self

                )

            except Exception as ex:

                LOGGER.exception(

                    "Registry listener failed: %s",

                    ex

                )

    # =============================================================================
    # REGISTER ENTITY
    # =============================================================================

    def register(
            self,
            *,
            entity_type: str,
            name: str,
            provider: str,
            external_id: str | None = None,
            description: str = "",
            aliases: list[str] | None = None,
            metadata: dict | None = None
    ) -> RegistryEntity:
        """
        Registers a canonical entity.

        If entity already exists,
        registry enriches it instead
        of creating duplicate.
        """
        normalized = self.normalize_name(name)
        #
        # Already exists by name
        #

        if normalized in self._by_name:

            entity = self._entities[
                self._by_name[normalized]
            ]
            entity.sources.add(provider)
            entity.updated_at = datetime.utcnow()
            if description and not entity.description:
                entity.description = description

            if metadata:
                entity.metadata.update(metadata)

            if aliases:
                entity.aliases.update(aliases)

            if external_id:
                entity.external_ids[
                    provider
                ] = external_id

                self._external_index[
                    self.make_external_key(
                        provider,
                        external_id
                    )
                ] = entity.uid

            self._history.append({
                "event": "update",
                "entity": entity.uid,
                "provider": provider,
                "timestamp": datetime.utcnow()
            })

            self.notify(
                event="entity_registered",
                entity=entity
            )

            return entity

        #
        # Create new
        #

        uid = self.new_uid()
        entity = RegistryEntity(
            uid=uid,
            entity_type=entity_type,
            name=name,
            description=description
        )

        entity.sources.add(provider)
        if aliases:
            entity.aliases.update(aliases)
        if metadata:
            entity.metadata.update(metadata)
        if external_id:
            entity.external_ids[
                provider
            ] = external_id

            self._external_index[
                self.make_external_key(
                    provider,
                    external_id
                )
            ] = uid

        #
        # Save
        #

        self._entities[uid] = entity

        self._by_type[
            entity_type
        ].add(uid)

        self._by_name[
            normalized
        ] = uid

        #
        # Alias index
        #

        for alias in entity.aliases:
            self._alias_index[
                self.normalize_name(alias)
            ] = uid

        #
        # Audit
        #

        self._history.append({
            "event": "create",
            "entity": uid,
            "provider": provider,
            "timestamp": datetime.utcnow()
        })
        return entity

    # =============================================================================
    # SEARCH
    #=============================================================================

    def exists(self, entity_type: str, name: str) -> bool:
        """
        Checks whether canonical entity exists.
        """
        normalized = self.normalize_name(name)
        if normalized not in self._by_name:
            return False
        uid = self._by_name[normalized]
        entity = self._entities.get(uid)
        if entity is None:
            return False
        return entity.entity_type == entity_type

    # -------------------------------------------------------------------------

    def get(self, uid: str) -> RegistryEntity | None:
        """
        Returns entity by internal UID.
        """
        return self._entities.get(uid)

    # -------------------------------------------------------------------------

    def find(self, entity_type: str, name: str) -> RegistryEntity | None:
        """
        Finds canonical entity by name.
        """
        normalized = self.normalize_name(name)
        uid = self._by_name.get(normalized)
        if uid is None:
            return None
        entity = self._entities.get(uid)
        if entity is None:
            return None
        if entity.entity_type != entity_type:
            return None
        return entity

    # -------------------------------------------------------------------------

    def find_by_alias(self, alias: str) -> RegistryEntity | None:
        """
        Search entity by alias.
        """
        normalized = self.normalize_name(alias)
        uid = self._alias_index.get(normalized)
        if uid is None:
            return None
        return self._entities.get(uid)

    # -------------------------------------------------------------------------

    def find_by_external_id(
            self,
            provider: str,
            external_id: str
    ) -> RegistryEntity | None:
        """
        Search entity by provider identifier.
        """

        uid = self._external_index.get(

            self.make_external_key(

                provider,

                external_id

            )

        )

        if uid is None:
            return None

        return self._entities.get(uid)

    # -------------------------------------------------------------------------

    def by_type(
            self,
            entity_type: str
    ) -> list[RegistryEntity]:
        """
        Returns all entities of specified type.
        """

        return [

            self._entities[uid]

            for uid

            in self._by_type.get(

                entity_type,

                set()

            )

        ]

    # -------------------------------------------------------------------------

    def all(self) -> list[RegistryEntity]:
        """
        Returns every registered entity.
        """

        return list(

            self._entities.values()

        )

    # -------------------------------------------------------------------------

    def count(
            self,
            entity_type: str | None = None
    ) -> int:
        """
        Registry statistics.
        """

        if entity_type is None:
            return len(

                self._entities

            )

        return len(

            self._by_type.get(

                entity_type,

                set()

            )

        )

    # -------------------------------------------------------------------------

    def entity_types(
            self
    ) -> list[str]:

        return sorted(

            self._by_type.keys()

        )

    # =============================================================================
    #
    # PERSISTENCE
    #
    # =============================================================================

    def clear(self) -> None:
        """
        Clears entire runtime registry.

        Database is NOT affected.

        Used before rebuilding registry
        from persistent storage.
        """

        self._entities.clear()
        self._by_name.clear()
        self._by_type.clear()
        self._external_index.clear()
        self._alias_index.clear()
        self._history.clear()
        self.notify(event="registry_cleared")

    # ---------------------------------------------------------------------

    def rebuild_indexes(self) -> None:
        """
        Rebuilds every runtime index.

        Used after loading entities
        from database.
        """

        self._by_name.clear()

        self._by_type.clear()

        self._alias_index.clear()

        self._external_index.clear()

        for uid, entity in self._entities.items():

            #
            # Name
            #

            self._by_name[
                self.normalize_name(
                    entity.name
                )
            ] = uid

            #
            # Type
            #

            self._by_type[
                entity.entity_type
            ].add(uid)

            #
            # Aliases
            #

            for alias in entity.aliases:
                self._alias_index[
                    self.normalize_name(alias)
                ] = uid

            #
            # External IDs
            #

            for provider, external_id in entity.external_ids.items():
                self._external_index[
                    self.make_external_key(
                        provider,
                        external_id
                    )
                ] = uid

    # ---------------------------------------------------------------------

    def statistics(self) -> dict:
        """
        Registry statistics.
        """

        return {

            "entities": len(self._entities),

            "entity_types": {

                entity_type: len(uids)

                for entity_type, uids

                in self._by_type.items()

            },

            "aliases": len(self._alias_index),

            "external_ids": len(self._external_index),

            "history": len(self._history)

        }

    # ---------------------------------------------------------------------

    def history(self) -> list[dict]:
        """
        Returns audit history.
        """

        return list(self._history)

    # ---------------------------------------------------------------------

    def validate(self) -> list[str]:
        """
        Performs registry consistency validation.
        """

        issues = []

        #
        # Duplicate canonical names
        #

        names = {}

        for entity in self._entities.values():

            key = self.normalize_name(entity.name)

            if key in names:
                issues.append(

                    f"Duplicate canonical name: {entity.name}"
                )
            names[key] = entity.uid
        #
        # Broken external references
        #
        for key, uid in self._external_index.items():
            if uid not in self._entities:
                issues.append(
                    f"Broken external index: {key}"

                )
        return issues

    def graph(self):
        """
        Return runtime graph.

        Automatically rebuilds
        if registry changed.
        """