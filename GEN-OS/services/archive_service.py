"""
===============================================================================
 GENESIS HR®
 GEN-OS

 FILE ---- services/archive_service.py
 BUILD ----- 0.2.1
 DESCRIPTION
  -----------
 Universal archive service.

 Supports:
    • ZIP extraction
    • SHA256
    • Manifest generation
    • Archive validation
 Every Provider delegates archive operations
 to this service.

===============================================================================
"""

from __future__ import annotations

import hashlib
import json
import logging
import zipfile

from pathlib import Path

LOGGER = logging.getLogger("GEN-OS.ArchiveService")


class ArchiveService:
    """
    Universal archive helper.
    No business logic.
    No knowledge about ESCO,
    O*NET or any dataset.
    Pure archive operations.
    """

    # ------------------------------------------------------------------

    @staticmethod
    def archives(folder: Path) -> list[Path]:
        """
        Return every ZIP archive.
        """
        if not folder.exists():
            return []
        return sorted(
            folder.glob("*.zip")
        )

    # ------------------------------------------------------------------

    @staticmethod
    def archive(folder: Path) -> Path:
        """
        Return first archive.
        Raises
        ------
        FileNotFoundError
        """

        archives = ArchiveService.archives(
            folder
        )
        if not archives:
            raise FileNotFoundError(
                f"No archive found in "
                f"{folder}"
            )
        return archives[0]

    # ------------------------------------------------------------------

    @staticmethod
    def extracted(folder: Path) -> Path:
        """
        Return extraction directory.
        """
        return folder / "extracted"

    # ------------------------------------------------------------------

    @staticmethod
    def ensure(folder: Path) -> Path:
        """
        Create extraction directory.
        """
        target = ArchiveService.extracted(
            folder
        )
        target.mkdir(
            parents=True,
            exist_ok=True
        )
        return target

    # ------------------------------------------------------------------

    @staticmethod
    def exists(folder: Path) -> bool:
        """
        Archive exists?
        """
        try:
            ArchiveService.archive(folder)
            return True
        except FileNotFoundError:
            return False

    # ------------------------------------------------------------------

    @staticmethod
    def sha256(path: Path) -> str:
        """
        SHA256 checksum.
        """
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            while True:
                chunk = stream.read(
                    1024 * 1024
                )
                if not chunk:
                    break
                digest.update(chunk)
        return digest.hexdigest()

    # ------------------------------------------------------------------

    @staticmethod
    def extract(folder: Path) -> Path:
        """
        Extract archive.
        Returns extraction folder.
        """
        archive = ArchiveService.archive(
            folder
        )
        destination = ArchiveService.ensure(
            folder
        )
        LOGGER.info(
            "Extracting %s",
            archive.name
        )

        with zipfile.ZipFile(
                archive
        ) as zip_file:
            zip_file.extractall(
                destination
            )
        return destination

    # ------------------------------------------------------------------

    @staticmethod
    def manifest_path(folder: Path) -> Path:
        """
        Path to manifest.json.
        """
        return folder / "manifest.json"

    # ------------------------------------------------------------------

    @staticmethod
    def metadata_path(folder: Path) -> Path:
        """
        Path to metadata.json.
        """
        return folder / "metadata.json"

    # ------------------------------------------------------------------

    @staticmethod
    def create_manifest(
            folder: Path,
            provider: str,
            version: str,
            homepage: str = "",
            vendor: str = "",
            description: str = ""
    ) -> Path:
        """
        Create dataset manifest.
        This file is static and describes
        dataset identity.
        """
        archive = ArchiveService.archive(folder)
        manifest = {
            "provider": provider,
            "version": version,
            "vendor": vendor,
            "homepage": homepage,
            "description": description,
            "archive": archive.name,
            "checksum": ArchiveService.sha256(
                archive
            )
        }
        path = ArchiveService.manifest_path(
            folder
        )
        path.write_text(
            json.dumps(
                manifest,
                indent=4,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )
        LOGGER.info("Manifest created: %s", path)
        return path

    # ------------------------------------------------------------------

    @staticmethod
    def create_metadata(
            folder: Path
    ) -> Path:
        """
        Scan extracted dataset and create
        metadata.json
        """
        extracted = ArchiveService.extracted(folder)
        files = []
        for file in extracted.rglob("*"):
            if file.is_file():
                files.append({
                    "name": file.name,
                    "relative": str(file.relative_to(extracted)),
                    "size": file.stat().st_size})
        metadata = {"files": files, "count": len(files)}
        path = ArchiveService.metadata_path(folder)
        path.write_text(
            json.dumps(
                metadata,
                indent=4,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        LOGGER.info("Metadata created: %s", path)
        return path

    # ------------------------------------------------------------------

    @staticmethod
    def extracted_files(folder: Path) -> list[Path]:
        """
        Return every extracted file.
        """
        extracted = ArchiveService.extracted(folder)
        if not extracted.exists():
            return []
        return sorted(
            file
            for file in extracted.rglob("*")
            if file.is_file()
        )

    # ------------------------------------------------------------------

    @staticmethod
    def has_file(folder: Path, filename: str) -> bool:
        """
        Dataset contains file?
        """

        return any(file.name == filename
                   for file in ArchiveService.extracted_files(folder))

    # ------------------------------------------------------------------

    @staticmethod
    def require(
            folder: Path,
            *filenames: str
    ) -> bool:
        """
        Validate required dataset files.
        """

        existing = {

            file.name

            for file in ArchiveService.extracted_files(
                folder
            )

        }

        return all(

            filename in existing

            for filename in filenames

        )

    # ------------------------------------------------------------------

    @staticmethod
    def validate_zip(
            folder: Path
    ) -> bool:
        """
        Check archive integrity.
        """

        archive = ArchiveService.archive(folder)

        try:

            with zipfile.ZipFile(
                    archive
            ) as zip_file:

                result = zip_file.testzip()

                if result is not None:
                    LOGGER.error(

                        "Broken ZIP member: %s",

                        result

                    )

                    return False

        except zipfile.BadZipFile:

            LOGGER.exception(
                "Invalid ZIP archive."
            )

            return False

        return True

    # ------------------------------------------------------------------

    @staticmethod
    def install(
            folder: Path
    ) -> Path:
        """
        Full installation pipeline.

            Validate ZIP

                ↓

            Extract

                ↓

            Build metadata

        """

        if not ArchiveService.validate_zip(
                folder
        ):
            raise RuntimeError(
                "Archive validation failed."
            )

        destination = ArchiveService.extract(
            folder
        )

        ArchiveService.create_metadata(
            folder
        )

        LOGGER.info(

            "Archive installed: %s",

            folder

        )

        return destination

    # ------------------------------------------------------------------

    @staticmethod
    def cleanup(
            folder: Path
    ) -> None:
        """
        Remove extracted directory.
        """

        import shutil

        extracted = ArchiveService.extracted(
            folder
        )

        if extracted.exists():
            shutil.rmtree(
                extracted
            )

            LOGGER.info(

                "Extraction directory removed."

            )

    # ------------------------------------------------------------------

    @staticmethod
    def summary(
            folder: Path
    ) -> dict:
        """
        Archive summary.
        """

        archive = ArchiveService.archive(folder)
        return {
            "archive": archive.name,
            "checksum": ArchiveService.sha256(archive),
            "size": archive.stat().st_size,
            "installed": ArchiveService.extracted(folder).exists(),
            "files": len(ArchiveService.extracted_files(folder))
        }
