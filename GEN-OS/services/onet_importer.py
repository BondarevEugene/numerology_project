"""
===============================================================

GEN-OS

O*NET Import Service

Build 0302

===============================================================
"""

from __future__ import annotations

from pathlib import Path

from services.dataset_loader import dataset_loader
from repositories.profession_repository import profession_repository
from repositories.skill_repository import skill_repository
from services.knowledge_graph_service import knowledge_graph
from models.knowledge_edge import KnowledgeEdge


class ONetImporter:
    """
    Imports O*NET datasets into GEN-OS.
    """

    def __init__(
        self,
        dataset_root: str | Path
    ):
        self.root = Path(dataset_root)

    # ---------------------------------------------------------

    def dataset(
        self,
        filename: str
    ) -> Path:
        return self.root / filename

    # ---------------------------------------------------------

    def exists(
        self,
        filename: str
    ) -> bool:
        return self.dataset(filename).exists()

    # ---------------------------------------------------------

    def extract_archive(
        self,
        archive_name: str,
        destination: str | Path
    ):
        archive = self.dataset(archive_name)
        return dataset_loader.extract_zip(archive, destination)

    # ---------------------------------------------------------

    def sql(
        self,
        database: str,
        query: str
    ):
        return dataset_loader.load_sql(self.dataset(database), query)

    # ---------------------------------------------------------

    def excel(
        self,
        filename: str
    ):
        return dataset_loader.load_excel(self.dataset(filename))

    # ---------------------------------------------------------

    def xml(
        self,
        filename: str
    ):
        return dataset_loader.load_xml(self.dataset(filename))

    # ---------------------------------------------------------

    def summary(self):
        return {
            "dataset": str(self.root),
            "files": len(list(self.root.glob("*")))
        }

    # ---------------------------------------------------------
    # PROFESSIONS
    # ---------------------------------------------------------

    def import_professions(
        self,
        records: list[dict]
    ) -> int:
        """
        Import occupations.
        """
        from models.profession import Profession

        imported = 0

        for row in records:
            occupation_id = str(
                row.get("occupation_id")
                or row.get("onet_soc_code")
                or row.get("code")
                or row.get("id")
                or ""
            ).strip()

            title = (
                row.get("title")
                or row.get("occupation")
                or row.get("name")
                or ""
            ).strip()

            if not occupation_id or not title:
                continue

            if profession_repository.get(occupation_id):
                continue

            profession = Profession(
                id=occupation_id,
                name=title,
                source="O*NET"
            )

            profession_repository.add(profession)
            knowledge_graph.add_node(profession)
            imported += 1

        return imported

    # ---------------------------------------------------------
    # SOFTWARE SKILLS
    # ---------------------------------------------------------

    def import_software_skills(
        self,
        records: list[dict]
    ) -> int:
        """
        Profession -> Software Skill
        """
        from models.skill import Skill

        imported = 0

        for row in records:
            profession_id = str(
                row.get("occupation_id")
                or row.get("onet_soc_code")
                or ""
            ).strip()

            technology = (
                row.get("software")
                or row.get("commodity_title")
                or row.get("technology")
                or row.get("title")
                or ""
            ).strip()

            if not profession_id or not technology:
                continue

            skill = skill_repository.find_by_name(technology)

            if skill is None:
                skill = Skill(
                    id=f"TECH::{technology.lower()}",
                    name=technology,
                    category="Technology",
                    source="O*NET"
                )
                skill_repository.add(skill)
                knowledge_graph.add_node(skill)

            knowledge_graph.connect(
                profession_id,
                skill.id,
                relation="USES"
            )
            imported += 1

        return imported

    # ---------------------------------------------------------
    # ESSENTIAL SKILLS (ВЕРНУТ В СТРУКТУРУ КЛАССА ONetImporter)
    # ---------------------------------------------------------

    def import_essential_skills(
        self,
        records: list[dict]
    ) -> int:
        imported = 0

        for row in records:
            profession_id = str(
                row.get("occupation_id")
                or row.get("onet_soc_code")
                or ""
            ).strip()

            skill_name = (
                row.get("skill")
                or row.get("element_name")
                or row.get("title")
                or ""
            ).strip()

            if not profession_id or not skill_name:
                continue

            skill_id = f"SKILL::{skill_name.lower()}"
            skill = skill_repository.get(skill_id)

            if skill is None:
                from models.skill import Skill
                skill = Skill(
                    id=skill_id,
                    name=skill_name,
                    category="Essential"
                )
                skill_repository.add(skill)
                knowledge_graph.add_node(skill)

            edge = KnowledgeEdge(
                source=profession_id,
                target=skill.id,
                relation="REQUIRES",
                weight=float(row.get("importance", 1))
            )

            knowledge_graph.add_edge(edge)
            imported += 1

        return imported

    # ---------------------------------------------------------
    # TRANSFERABLE SKILLS (ВЕРНУТ В СТРУКТУРУ КЛАССА ONetImporter)
    # ---------------------------------------------------------

    def import_transferable_skills(
        self,
        records: list[dict]
    ) -> int:
        imported = 0

        for row in records:
            profession_id = str(
                row.get("occupation_id")
                or row.get("onet_soc_code")
                or ""
            ).strip()

            skill_name = (
                row.get("skill")
                or row.get("title")
                or ""
            ).strip()

            if not profession_id or not skill_name:
                continue

            skill_id = f"TRANSFER::{skill_name.lower()}"
            skill = skill_repository.get(skill_id)

            if skill is None:
                from models.skill import Skill
                skill = Skill(
                    id=skill_id,
                    name=skill_name,
                    category="Transferable"
                )
                skill_repository.add(skill)
                knowledge_graph.add_node(skill)

            edge = KnowledgeEdge(
                source=profession_id,
                target=skill.id,
                relation="TRANSFERABLE",
                weight=float(row.get("importance", 1))
            )

            knowledge_graph.add_edge(edge)
            imported += 1

        return imported

    # ---------------------------------------------------------
    # IMPORT ALL (ВЕРНУТ В СТРУКТУРУ КЛАССА ONetImporter)
    # ---------------------------------------------------------

    def import_all(
        self,
        datasets: dict
    ) -> dict:
        """
        Execute complete O*NET import.

        datasets example:
        {
            "professions": [...],
            "software": [...],
            "essential": [...],
            "transferable": [...]
        }
        """
        stats = {
            "professions": 0,
            "software": 0,
            "essential": 0,
            "transferable": 0
        }

        if "professions" in datasets:
            stats["professions"] = self.import_professions(
                datasets["professions"]
            )

        if "software" in datasets:
            stats["software"] = self.import_software_skills(
                datasets["software"]
            )

        if "essential" in datasets:
            stats["essential"] = self.import_essential_skills(
                datasets["essential"]
            )

        if "transferable" in datasets:
            stats["transferable"] = self.import_transferable_skills(
                datasets["transferable"]
            )

        stats["graph"] = knowledge_graph.statistics()
        return stats


# ==========================================================
# GLOBAL SINGLETON (ВЫНЕСЕН ИЗ КЛАССА НА УРОВЕНЬ МОДУЛЯ)
# ==========================================================

onet_importer = ONetImporter(
    "datasets/onet"
)

# ==============================================================
# END OF FILE // OMNIFACTORY LABS COGNITIVE REPOSITORY SPEC
# ==============================================================
