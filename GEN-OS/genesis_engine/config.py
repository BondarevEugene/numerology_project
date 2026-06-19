"""
Genesis configuration.

Single source of truth.
"""

from pathlib import Path

ROOT = Path(__file__).parent

CACHE = ROOT / "cache"

DATASETS = ROOT / "datasets"

EXPORT = ROOT / "export"

LOGS = ROOT / "logs"

REGISTRY = ROOT / "registry"

TESTS = ROOT / "tests"


CACHE_PATH

EXPORT_PATH

REGISTRY_PATH

PROVIDER_TIMEOUT

RETRY_COUNT

SUPPORTED_LANGUAGES

SUPPORTED_PROVIDERS