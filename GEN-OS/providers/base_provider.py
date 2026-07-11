"""
===============================================================================

 GENESIS HR®
 GEN-OS

 FILE
 ----
 providers/base_provider.py

 BUILD
 -----
 0.2.1

 DESCRIPTION
 -----------
 Abstract base class for every platform resource provider.

 RESPONSIBILITY
 --------------
 • Dataset discovery
 • Dataset validation
 • Dataset loading
 • Metadata generation

 NOTE
 ----
 Archive handling is delegated to ArchiveService.

===============================================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from pathlib import Path

import logging


LOGGER = logging.getLogger("GEN-OS.Provider")


class ResourceProvider(ABC):
    """
    Base class for every platform provider.

    Provider lifecycle

        discover()

            ↓

        install()

            ↓

        validate()

            ↓

        load()

    Concrete implementations:

        ESCOProvider

        ONETProvider

        LinkedInProvider

        WorkUAProvider

        DjinniProvider
    """

    def __init__(
        self,
        dataset_root: Path
    ) -> None:

        self._root = Path(dataset_root)

    # ------------------------------------------------------------------

    @property
    def root(self) -> Path:
        """
        Dataset root directory.
        """

        return self._root

    # ------------------------------------------------------------------

    @property
    def extracted(self) -> Path:
        """
        Extracted dataset directory.
        """

        return self.root / "extracted"

    # ------------------------------------------------------------------

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Provider identifier.
        """

    # ------------------------------------------------------------------

    @property
    @abstractmethod
    def version(self) -> str:
        """
        Dataset version.
        """

    # ------------------------------------------------------------------

    @abstractmethod
    def discover(self) -> bool:
        """
        Returns True if dataset exists.
        """

    # ------------------------------------------------------------------

    @abstractmethod
    def install(self) -> None:
        """
        Prepare provider resources.

        Archive extraction is usually delegated
        to ArchiveService.
        """

    # ------------------------------------------------------------------

    @abstractmethod
    def validate(self) -> bool:
        """
        Validate dataset structure.
        """

    # ------------------------------------------------------------------

    @abstractmethod
    def metadata(self) -> dict:
        """
        Provider metadata.
        """

    # ------------------------------------------------------------------

    @abstractmethod
    def load(self):
        """
        Load provider entities.
        """

    # ------------------------------------------------------------------

    @abstractmethod
    def statistics(self) -> dict:
        """
        Runtime statistics.
        """

    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (

            f"<{self.__class__.__name__}"

            f" name='{self.name}'"

            f" version='{self.version}'>"

        )
    # ------------------------------------------------------------------

    def exists(self) -> bool:
        """
        Returns True if dataset root exists.
        """

        return self.root.exists()

    # ------------------------------------------------------------------

    def ensure_directory(self) -> None:
        """
        Ensure extracted directory exists.
        """

        self.extracted.mkdir(
            parents=True,
            exist_ok=True
        )

    # ------------------------------------------------------------------

    def dataset_files(
        self,
        pattern: str = "*"
    ) -> list[Path]:
        """
        Return extracted dataset files.
        """

        if not self.extracted.exists():
            return []

        return sorted(
            self.extracted.rglob(pattern)
        )

    # ------------------------------------------------------------------

    def file(
        self,
        filename: str
    ) -> Path:
        """
        Locate a file inside extracted dataset.

        Raises
        ------
        FileNotFoundError
        """

        for path in self.dataset_files():

            if path.name == filename:
                return path

        raise FileNotFoundError(
            f"{filename} not found in "
            f"{self.extracted}"
        )

    # ------------------------------------------------------------------

    def has_file(
        self,
        filename: str
    ) -> bool:
        """
        Check whether a dataset contains
        a specific file.
        """

        try:

            self.file(filename)

            return True

        except FileNotFoundError:

            return False

    # ------------------------------------------------------------------

    def require(
        self,
        *filenames: str
    ) -> bool:
        """
        Validate required dataset files.
        """

        return all(

            self.has_file(name)

            for name in filenames

        )

    # ------------------------------------------------------------------

    def info(self) -> dict:
        """
        Common provider information.
        """

        return {

            "provider": self.name,

            "version": self.version,

            "root": str(self.root),

            "extracted": str(
                self.extracted
            )

        }

    # ------------------------------------------------------------------

    def statistics(self) -> dict:
        """
        Default statistics.

        Child classes may extend it.
        """

        return {

            **self.info(),

            "files": len(
                self.dataset_files()
            )

        }