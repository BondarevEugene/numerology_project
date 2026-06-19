"""
═══════════════════════════════════════════════════════
GENESIS
Knowledge Import Launcher
═══════════════════════════════════════════════════════
"""

from genesis_engine.importers.profession_importer import (
    ProfessionImporter
)


def main():
    registry = ProfessionImporter.import_json(
        "datasets/professions.json"
    )

    print()
    print("═══════════════════════════════")
    print("Registry Statistics")
    print()
    print(
        registry.statistics()
    )
    print()
    print("═══════════════════════════════")


if __name__ == "__main__":
    main()