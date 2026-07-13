# ==============================================================================
# PROJECT: OMNIFACTORY PLATFORM
# MODULE: Export Engine
# FILE: core/compiler/exporter.py
# VERSION: 2.0
# ==============================================================================
# PURPOSE
# ------------------------------------------------------------------------------
# Export Engine отвечает за создание структуры проекта.
# Он НЕ знает содержимого файлов.
# Каждый файл генерируется собственным Exporter.
# ==============================================================================

from pathlib import Path

from core.compiler.exporters.readme import ReadmeExporter
from core.compiler.exporters.requirements import RequirementsExporter
from core.compiler.exporters.docker import DockerExporter
from core.compiler.exporters.runtime_json import RuntimeExporter
from core.compiler.exporters.manifest import ManifestExporter
from core.compiler.exporters.gitignore import GitIgnoreExporter


class Exporter:
    """
    Центральный координатор экспорта.
    """

    def __init__(self):
        self.exporters = [
            ReadmeExporter(),
            RequirementsExporter(),
            DockerExporter(),
            RuntimeExporter(),
            ManifestExporter(),
            GitIgnoreExporter()
        ]

    # ----------------------------------------------------------------------

    def export(self, project_path: Path):
        project_path.mkdir(
            parents=True,
            exist_ok=True
        )
        self._create_structure(project_path)
        for exporter in self.exporters:
            exporter.generate(project_path)
        return {
            "success": True,
            "location": str(project_path)
        }

    # ----------------------------------------------------------------------

    def _create_structure(self, root: Path):
        directories = [
            "app",
            "api",
            "routers",
            "services",
            "core",
            "config",
            "static",
            "templates",
            "tests",
            "workspace",
            "logs",
            "docker"
        ]

        for directory in directories:
            (root / directory).mkdir(
                parents=True,
                exist_ok=True
            )
