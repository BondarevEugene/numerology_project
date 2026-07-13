"""
════════════════════════════════════════════════════════════════════════════════════
 GENESIS HR® // OMNIFACTORY EVO

 GEN-OS Platform
 MODULE:     Knowledge Management Center
 COMPONENT:     Source Manager
 FILE:     source_manager.py
 BUILD:     0401
 STATUS:     Enterprise Foundation
 DESCRIPTION
────────────────────────────────────────────────────────────────────────────────

 Source Manager controls every external knowledge provider connected
 to GEN-OS.

 It does NOT import datasets.
 It does NOT parse datasets.
 It does NOT build Knowledge Graph.

 Responsibilities

    • Register providers
    • Enable / Disable providers
    • Store provider configuration
    • Check provider availability
    • Track synchronization
    • Keep provider statistics

 Supported providers

    • O*NET
    • ESCO
    • ASPECTT
    • CareerOneStop
    • Local Folder
    • ZIP Packages
    • REST API
    • PostgreSQL
    • Future Providers

════════════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any
from typing import Optional
import requests

from .import_session import ImportSession
from .import_session import ImportStatus

from .validation_engine import ValidationEngine

from .normalization_engine import NormalizationEngine

from registry.registry_loader import RegistryLoader

# ==============================================================================
# SOURCE STATUS
# ==============================================================================

class SourceStatus(str, Enum):
    UNKNOWN = "UNKNOWN"
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DISABLED = "DISABLED"
    SYNCING = "SYNCING"


# ==============================================================================
# SOURCE TYPE
# ==============================================================================


class SourceType(str, Enum):
    LOCAL = "LOCAL"
    REST = "REST"
    ZIP = "ZIP"
    DATABASE = "DATABASE"
    CUSTOM = "CUSTOM"


# ==============================================================================
# KNOWLEDGE SOURCE
# ==============================================================================


@dataclass(slots=True)
class KnowledgeSource:
    """
    Canonical description of external provider.
    """
    #
    # Identity
    #
    source_id: str
    name: str
    provider_type: SourceType
    #
    # Location
    #
    location: str = ""
    api_url: str = ""
    #
    # General
    #
    version: str = ""
    description: str = ""
    enabled: bool = True
    readonly: bool = True
    auto_sync: bool = False
    priority: int = 100
    #
    # Runtime
    #
    status: SourceStatus = SourceStatus.UNKNOWN
    last_sync: Optional[datetime] = None
    last_error: str = ""
    #
    # Statistics
    #
    dataset_count: int = 0
    entity_count: int = 0
    relation_count: int = 0
    #
    # Metadata
    #
    metadata: dict[str, Any] = field(default_factory=dict)
    #
    # Audit
    #
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(
        default_factory=datetime.utcnow)


# ==============================================================================
# SOURCE MANAGER
# ==============================================================================


class SourceManager:
    """
    Central registry of every external knowledge provider.
    """

    def __init__(self) -> None:
        #
        # Providers
        #
        self._sources: dict[str, KnowledgeSource] = {}
        #
        # Audit events
        #
        self._events: list[dict] = []
        #
        # Configuration version
        #
        self.config_version = 1

        self.validator = ValidationEngine()

        self.normalizer = NormalizationEngine()

        self.registry_loader = RegistryLoader()
    # -------------------------------------------------------------------------

    def register(self, source: KnowledgeSource) -> KnowledgeSource:
        """
        Register provider.
        """
        self._sources[source.source_id] = source
        source.updated_at = datetime.utcnow()
        self._events.append({
            "event": "REGISTER",
            "source": source.source_id,
            "time": datetime.utcnow()
        })

        return source

    # -------------------------------------------------------------------------

    def remove(self, source_id: str) -> bool:
        """
        Remove provider.
        """
        if source_id not in self._sources:
            return False
        del self._sources[source_id]
        self._events.append({
            "event": "REMOVE",
            "source": source_id,
            "time": datetime.utcnow()
        })
        return True

    # -------------------------------------------------------------------------

    def get(self, source_id: str) -> Optional[KnowledgeSource]:
        return self._sources.get(source_id)

    # -------------------------------------------------------------------------

    def exists(self, source_id: str) -> bool:
        return source_id in self._sources

    # -------------------------------------------------------------------------

    def all(self) -> list[KnowledgeSource]:
        return sorted(
            self._sources.values(),
            key=lambda item: item.priority
        )

    # -------------------------------------------------------------------------
    # ENABLE
    # -------------------------------------------------------------------------

    def enable(self, source_id: str) -> bool:
        """
        Enable provider.
        """
        source = self.get(source_id)
        if source is None:
            return False
        source.enabled = True
        source.updated_at = datetime.utcnow()
        self._events.append({
            "event": "ENABLE",
            "source": source.source_id,
            "time": datetime.utcnow()
        })
        return True

    # -------------------------------------------------------------------------
    # DISABLE
    # -------------------------------------------------------------------------

    def disable(self, source_id: str) -> bool:
        """
        Disable provider.
        """
        source = self.get(source_id)
        if source is None:
            return False
        source.enabled = False
        source.status = SourceStatus.DISABLED
        source.updated_at = datetime.utcnow()
        self._events.append({
            "event": "DISABLE",
            "source": source.source_id,
            "time": datetime.utcnow()
        })
        return True

    # -------------------------------------------------------------------------
    # LOCAL CHECK
    # -------------------------------------------------------------------------

    def _check_local(self, source: KnowledgeSource) -> bool:
        """
        Verify local dataset location.
        """
        path = Path(source.location)
        if not path.exists():
            source.status = SourceStatus.ERROR
            source.last_error = "Directory not found"
            return False
        if not path.is_dir():
            source.status = SourceStatus.ERROR
            source.last_error = "Path is not a directory"
            return False
        source.status = SourceStatus.ONLINE
        source.last_error = ""
        return True

    # -------------------------------------------------------------------------
    # REST CHECK
    # -------------------------------------------------------------------------

    def _check_rest(self, source: KnowledgeSource) -> bool:
        """
        Verify REST endpoint availability.
        """
        try:
            response = requests.get(
                source.api_url,
                timeout=5
            )
            if response.status_code < 400:
                source.status = SourceStatus.ONLINE
                source.last_error = ""
                return True
            source.status = SourceStatus.ERROR
            source.last_error = (
                f"HTTP {response.status_code}"
            )
            return False
        except Exception as ex:
            source.status = SourceStatus.OFFLINE
            source.last_error = str(ex)
            return False

    # -------------------------------------------------------------------------
    # CHECK
    # -------------------------------------------------------------------------

    def check(self, source_id: str) -> bool:
        """
        Perform provider health check.
        """
        source = self.get(source_id)
        if source is None:
            return False
        if not source.enabled:
            source.status = SourceStatus.DISABLED
            return False
        source.status = SourceStatus.SYNCING
        if source.provider_type == SourceType.LOCAL:
            result = self._check_local(source)
        elif source.provider_type == SourceType.REST:
            result = self._check_rest(source)
        else:
            source.status = SourceStatus.WARNING
            source.last_error = ("Health check not implemented")
            result = False
        source.updated_at = datetime.utcnow()
        return result

    # -------------------------------------------------------------------------
    # CHECK ALL
    # -------------------------------------------------------------------------

    def check_all(self) -> None:
        """
        Verify every registered provider.
        """
        for source in self.all():
            self.check(source.source_id)

    # -------------------------------------------------------------------------
    # STATISTICS
    # -------------------------------------------------------------------------

    def statistics(self) -> dict:
        """
        Returns aggregated information about all registered providers.
        """
        stats = {
            "providers": len(self._sources),
            "enabled": 0,
            "disabled": 0,
            "online": 0,
            "offline": 0,
            "warning": 0,
            "error": 0,
            "syncing": 0,
            "datasets": 0,
            "entities": 0,
            "relations": 0
        }

        for source in self._sources.values():
            if source.enabled:
                stats["enabled"] += 1
            else:
                stats["disabled"] += 1
            if source.status == SourceStatus.ONLINE:
                stats["online"] += 1
            elif source.status == SourceStatus.OFFLINE:
                stats["offline"] += 1
            elif source.status == SourceStatus.WARNING:
                stats["warning"] += 1
            elif source.status == SourceStatus.ERROR:
                stats["error"] += 1
            elif source.status == SourceStatus.SYNCING:
                stats["syncing"] += 1
            stats["datasets"] += source.dataset_count
            stats["entities"] += source.entity_count
            stats["relations"] += source.relation_count
        return stats

    # -------------------------------------------------------------------------
    # EVENTS
    # -------------------------------------------------------------------------

    def events(self) -> list[dict]:
        """
        Returns audit events.
        """
        return list(self._events)

    # -------------------------------------------------------------------------
    # CLEAR EVENTS
    # -------------------------------------------------------------------------

    def clear_events(self) -> None:
        self._events.clear()

    # -------------------------------------------------------------------------
    # CONFIGURATION
    # -------------------------------------------------------------------------

    def export_configuration(self) -> list[dict]:
        """
        Export provider configuration.
        Used by Knowledge Management Center.
        """
        config = []
        for source in self.all():
            config.append({
                "source_id": source.source_id,
                "name": source.name,
                "provider_type": source.provider_type.value,
                "location": source.location,
                "api_url": source.api_url,
                "enabled": source.enabled,
                "readonly": source.readonly,
                "auto_sync": source.auto_sync,
                "priority": source.priority,
                "version": source.version,
                "description": source.description
            })
        return config

    # -------------------------------------------------------------------------
    # IMPORT CONFIGURATION
    # -------------------------------------------------------------------------

    def import_configuration(
            self,
            configuration: list[dict]
    ) -> None:
        """
        Restore providers from configuration.
        """
        self._sources.clear()

        for item in configuration:
            source = KnowledgeSource(
                source_id=item["source_id"],
                name=item["name"],
                provider_type=SourceType(
                    item["provider_type"]
                ),
                location=item.get(
                    "location",
                    ""
                ),
                api_url=item.get(
                    "api_url",
                    ""
                ),
                enabled=item.get(
                    "enabled",
                    True
                ),
                readonly=item.get(
                    "readonly",
                    True
                ),
                auto_sync=item.get(
                    "auto_sync",
                    False
                ),
                priority=item.get(
                    "priority",
                    100
                ),
                version=item.get(
                    "version",
                    ""
                ),
                description=item.get(
                    "description",
                    ""
                )
            )
            self.register(source)

    # -------------------------------------------------------------------------
    # FIND BY TYPE
    # -------------------------------------------------------------------------

    def find_by_type(
            self,
            provider_type: SourceType
    ) -> list[KnowledgeSource]:
        """
        Returns all providers of the specified type.
        """
        return sorted(
            [
                source
                for source in self._sources.values()
                if source.provider_type == provider_type
            ],
            key=lambda item: item.priority
        )

    # -------------------------------------------------------------------------
    # ENABLED PROVIDERS
    # -------------------------------------------------------------------------

    def enabled(self) -> list[KnowledgeSource]:
        """
        Returns enabled providers.
        """
        return sorted(
            [
                source
                for source in self._sources.values()
                if source.enabled
            ],
            key=lambda item: item.priority
        )

    # -------------------------------------------------------------------------
    # DISABLED PROVIDERS
    # -------------------------------------------------------------------------

    def disabled(self) -> list[KnowledgeSource]:
        """
        Returns disabled providers.
        """
        return sorted(
            [
                source
                for source in self._sources.values()
                if not source.enabled
            ],
            key=lambda item: item.priority

        )

    # -------------------------------------------------------------------------
    # ONLINE PROVIDERS
    # -------------------------------------------------------------------------

    def online(self) -> list[KnowledgeSource]:
        """
        Returns online providers.
        """
        return [
            source
            for source
            in self.enabled()
            if source.status == SourceStatus.ONLINE
        ]

    # -------------------------------------------------------------------------
    # OFFLINE PROVIDERS
    # -------------------------------------------------------------------------
    def offline(self) -> list[KnowledgeSource]:
        """
        Returns offline providers.
        """
        return [
            source
            for source
            in self.enabled()
            if source.status in (
                SourceStatus.ERROR,
                SourceStatus.OFFLINE
            )
        ]

    # -------------------------------------------------------------------------
    # RESET
    # -------------------------------------------------------------------------

    def reset(self) -> None:
        """
        Clears all providers.
        Intended for testing and development.
        """

        self._sources.clear()
        self._events.clear()

    # -------------------------------------------------------------------------
    # STRING REPRESENTATION
    # -------------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self._sources)

    def __contains__(
            self,
            source_id: str
    ) -> bool:
        return self.exists(source_id)

    def __iter__(self):
        return iter(self.all())

    def create_import_session(
            self,
            dataset_name: str,
            source_name: str,
            operator: str = "system"
    ) -> ImportSession:

        """
        Создает новую Import Session.

        Каждая загрузка датасета проходит через собственную
        независимую сессию.
        """

        import uuid

        session = ImportSession(

            session_id=str(uuid.uuid4()),

            dataset_name=dataset_name,

            source_name=source_name,

            created_by=operator

        )

        session.set_status(ImportStatus.CREATED)

        return session

    # -------------------------------------------------------------------------
    # DATA MANAGEMENT: Validation
    # -------------------------------------------------------------------------
    def validate_dataset(self, file_path):

        """
        Запускает Validation Engine.
        """

        return self.validator.validate(file_path)

    # -------------------------------------------------------------------------
    # DATA MANAGEMENT: normalization
    # -------------------------------------------------------------------------
    def normalize_dataset(
            self,
            dataframe
    ):

        """
        Запуск движка нормализации.
        """

        return self.normalizer.normalize_dataframe(
            dataframe
        )

    def load_into_registry(
            self,
            dataframe
    ):

        """
        Передает
        нормализованный DataFrame
        в Registry.
        """

        return self.registry_loader.load_dataframe(
            dataframe
        )