"""
===============================================================================

 GENESIS HR®
 GEN-OS

 FILE
 ----
 kernel/resource_manager.py

 BUILD
 -----
 0.2.0

 DESCRIPTION
 -----------
 Global platform Resource Manager.

 This class is the single entry point for every resource
 available inside GEN-OS.

 The manager DOES NOT know how datasets work.
 It only manages providers.

 AUTHOR
 ------
 Yevhenii Bondariev
 OpenAI GPT-5.5

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from pathlib import Path

from typing import Dict
from typing import Optional
from typing import Type
from typing import Iterable

import logging

LOGGER = logging.getLogger("GEN-OS.ResourceManager")


# =============================================================================
# Provider Protocol
# =============================================================================

class ResourceProvider:
    """
    Abstract provider contract.

    Every provider (ESCO, O*NET, LinkedIn, etc.)
    must implement this interface.
    """

    name: str = "provider"

    def discover(self) -> bool:
        raise NotImplementedError

    def install(self) -> None:
        raise NotImplementedError

    def validate(self) -> bool:
        raise NotImplementedError

    def metadata(self) -> dict:
        raise NotImplementedError


# =============================================================================
# Resource Descriptor
# =============================================================================

@dataclass(slots=True)
class ResourceRecord:
    """
    Registered platform resource.
    """
    identifier: str
    provider: ResourceProvider
    root: Path
    enabled: bool = True
    metadata: dict = field(default_factory=dict)

# =============================================================================
# Resource Manager
# =============================================================================

class ResourceManager:
    """
    Central registry of platform resources.
    The Kernel communicates ONLY with ResourceManager.
    Providers know everything about datasets.
    ResourceManager knows nothing about ESCO,
    O*NET or future providers.
    """

    def __init__(self, project_root: Path):
        self._root = Path(project_root)
        self._providers: Dict[
            str,
            ResourceProvider
        ] = {}
        self._resources: Dict[
            str,
            ResourceRecord
        ] = {}
        LOGGER.info(
            "ResourceManager initialized."
        )

    # -----------------------------------------------------------------

    @property
    def root(self) -> Path:
        return self._root

    # -----------------------------------------------------------------

    def register_provider(
            self,
            provider: ResourceProvider
    ) -> None:
        """
        Register provider.
        """

        LOGGER.info(
            "Register provider: %s",
            provider.name
        )

        self._providers[
            provider.name
        ] = provider

    # -----------------------------------------------------------------

    def provider(
            self,
            name: str
    ) -> ResourceProvider:
        """
        Get provider by name.
        """

        if name not in self._providers:
            raise KeyError(
                f"Provider '{name}' "
                "is not registered."
            )

        return self._providers[name]

    # -----------------------------------------------------------------

    def providers(
            self
    ) -> Iterable[ResourceProvider]:

        return self._providers.values()

    # -----------------------------------------------------------------

    def scan(self) -> None:
        """
        Scan every registered provider.
        """
        LOGGER.info(
            "Scanning resources..."
        )
        for provider in self.providers():
            LOGGER.info(
                "Scanning %s...",
                provider.name
            )
            if not provider.discover():
                LOGGER.warning(
                    "Dataset not found: %s",
                    provider.name
                )

                continue
            record = ResourceRecord(
                identifier=provider.name,
                provider=provider,
                root=self.root,
                metadata=provider.metadata()
            )
            self._resources[
                provider.name
            ] = record
        LOGGER.info(
            "Resource scan completed."
        )
    # -----------------------------------------------------------------

    def resource(
        self,
        identifier: str
    ) -> ResourceRecord:
        """
        Return registered resource.
        """

        if identifier not in self._resources:

            raise KeyError(
                f"Resource '{identifier}' "
                "is not registered."
            )

        return self._resources[identifier]

    # -----------------------------------------------------------------

    def has_resource(
        self,
        identifier: str
    ) -> bool:

        return identifier in self._resources

    # -----------------------------------------------------------------

    def enable(
        self,
        identifier: str
    ) -> None:
        """
        Enable resource.
        """

        self.resource(identifier).enabled = True

        LOGGER.info(
            "Resource enabled: %s",
            identifier
        )

    # -----------------------------------------------------------------

    def disable(
        self,
        identifier: str
    ) -> None:
        """
        Disable resource.
        """

        self.resource(identifier).enabled = False

        LOGGER.info(
            "Resource disabled: %s",
            identifier
        )

    # -----------------------------------------------------------------

    def install_all(self) -> None:
        """
        Install every discovered resource.
        """

        LOGGER.info(
            "Installing resources..."
        )

        for record in self.resources():

            if not record.enabled:
                continue

            LOGGER.info(
                "Installing '%s'",
                record.identifier
            )

            record.provider.install()

            record.metadata = (
                record.provider.metadata()
            )

        LOGGER.info(
            "Installation completed."
        )

    # -----------------------------------------------------------------

    def validate_all(self) -> bool:
        """
        Validate every installed resource.
        """

        LOGGER.info(
            "Validating resources..."
        )

        success = True

        for record in self.resources():

            if not record.enabled:
                continue

            valid = record.provider.validate()

            if not valid:

                LOGGER.error(
                    "Validation failed: %s",
                    record.identifier
                )

                success = False

            else:

                LOGGER.info(
                    "Validation OK: %s",
                    record.identifier
                )

        return success

    # -----------------------------------------------------------------

    def reload(self) -> None:
        """
        Rebuild provider registry.
        """

        LOGGER.info(
            "Reloading resource registry..."
        )

        self._resources.clear()

        self.scan()

    # -----------------------------------------------------------------

    @property
    def index_file(self) -> Path:
        """
        Kernel resource index.

        kernel/resource_index.json
        """

        return (
            self.root
            / "kernel"
            / "resource_index.json"
        )

    # -----------------------------------------------------------------

    def save_index(self) -> None:
        """
        Save current resource registry.
        """

        import json

        data = []

        for record in self.resources():

            data.append({

                "id":
                    record.identifier,

                "provider":
                    record.provider.name,

                "enabled":
                    record.enabled,

                "metadata":
                    record.metadata

            })

        self.index_file.write_text(

            json.dumps(
                data,
                indent=4,
                ensure_ascii=False
            ),

            encoding="utf-8"

        )

        LOGGER.info(
            "Resource index saved."
        )

    # -----------------------------------------------------------------

    def load_index(self) -> bool:
        """
        Restore saved resource index.

        Returns
        -------
        bool
            True if index exists.
        """

        import json

        if not self.index_file.exists():

            return False

        LOGGER.info(
            "Loading resource index..."
        )

        records = json.loads(

            self.index_file.read_text(
                encoding="utf-8"
            )

        )

        for item in records:

            provider_name = item["provider"]

            if provider_name not in self._providers:
                continue

            provider = self.provider(
                provider_name
            )

            self._resources[
                item["id"]
            ] = ResourceRecord(

                identifier=item["id"],

                provider=provider,

                root=self.root,

                enabled=item.get(
                    "enabled",
                    True
                ),

                metadata=item.get(
                    "metadata",
                    {}
                )

            )

        LOGGER.info(
            "Resource index restored."
        )

        return True
    # -----------------------------------------------------------------

    def boot(self) -> None:
        """
        Kernel resource initialization.

        Startup sequence:

            1. Restore resource index (if exists)
            2. Otherwise scan providers
            3. Validate resources
            4. Save fresh index
        """

        LOGGER.info(
            "Booting ResourceManager..."
        )

        restored = self.load_index()

        if not restored:

            self.scan()

        if not self.validate_all():

            LOGGER.warning(
                "Some resources failed validation."
            )

        self.save_index()

        LOGGER.info(
            "ResourceManager READY."
        )

    # -----------------------------------------------------------------

    def shutdown(self) -> None:
        """
        Shutdown Resource Manager.
        """

        LOGGER.info(
            "Saving resource registry..."
        )

        self.save_index()

        LOGGER.info(
            "ResourceManager stopped."
        )

    # -----------------------------------------------------------------

    def statistics(self) -> dict:
        """
        Runtime statistics.
        """

        enabled = sum(
            1
            for resource in self.resources()
            if resource.enabled
        )

        disabled = len(self._resources) - enabled

        return {

            "providers":
                len(self._providers),

            "resources":
                len(self._resources),

            "enabled":
                enabled,

            "disabled":
                disabled

        }

    # -----------------------------------------------------------------

    def clear(self) -> None:
        """
        Clear runtime registry.
        """

        LOGGER.info(
            "Clearing resource registry..."
        )

        self._resources.clear()

    # -----------------------------------------------------------------

    def __contains__(
        self,
        identifier: str
    ) -> bool:
        return identifier in self._resources

    # -----------------------------------------------------------------

    def __len__(self) -> int:
        return len(self._resources)

    # -----------------------------------------------------------------

    def __iter__(self):
        return iter(
            self._resources.values()
        )

    # -----------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"<ResourceManager "
            f"providers={len(self._providers)} "
            f"resources={len(self._resources)}>"
        )


# ==============================================================================
# FACTORY
# ==============================================================================


_RESOURCE_MANAGER: Optional[
    ResourceManager
] = None


def create_resource_manager(
    project_root: Path
) -> ResourceManager:
    """
    Create singleton ResourceManager.

    Parameters
    ----------
    project_root:
        GEN-OS project root.

    Returns
    -------
    ResourceManager
    """

    global _RESOURCE_MANAGER
    if _RESOURCE_MANAGER is None:
        _RESOURCE_MANAGER = ResourceManager(
            project_root
        )
    return _RESOURCE_MANAGER


# ==============================================================================
# GLOBAL INSTANCE
# ==============================================================================

resource_manager = create_resource_manager(
    Path(__file__).resolve().parent.parent
)