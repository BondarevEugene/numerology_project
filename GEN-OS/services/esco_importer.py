"""
===============================================================================

GENESIS HR®

ESCO Import Service

BUILD 0301

DESCRIPTION
-----------

Imports ESCO datasets into GEN-OS.

Supported:

    occupations.csv
    skills.csv
    relations.csv

===============================================================================
"""

from __future__ import annotations

from pathlib import Path

from models.profession import Profession
from models.skill import Skill
from models.knowledge_edge import KnowledgeEdge

from repositories.profession_repository import profession_repository
from repositories.skill_repository import skill_repository

from services.dataset_loader import dataset_loader
from services.knowledge_graph_service import knowledge_graph


class ESCOImporter:

    """
    ESCO Import Service.
    """

    def __init__(
        self,
        dataset_root: str | Path
    ):

        self.root = Path(dataset_root)

    # ----------------------------------------------------------------

    def dataset(
        self,
        filename: str
    ) -> Path:

        return self.root / filename

    # ----------------------------------------------------------------

    def csv(
        self,
        filename: str
    ) -> list[dict]:

        return dataset_loader.load_csv(

            self.dataset(filename)

        )

    # ----------------------------------------------------------------

    def exists(
        self,
        filename: str
    ) -> bool:

        return self.dataset(
            filename
        ).exists()

    # ----------------------------------------------------------------

    def import_occupations(
        self,
        rows: list[dict]
    ) -> int:

        imported = 0

        for row in rows:

            profession_id = str(

                row.get("conceptUri")
                or row.get("id")
                or row.get("uri")
                or ""

            ).strip()

            profession_name = (

                row.get("preferredLabel")
                or row.get("title")
                or row.get("name")
                or ""

            ).strip()

            if not profession_id:

                continue

            if not profession_name:

                continue

            if profession_repository.get(
                profession_id
            ):
                continue

            profession = Profession(

                id=profession_id,

                name=profession_name,

                category="ESCO",

                description=row.get(

                    "description",

                    ""

                )

            )

            profession_repository.add(
                profession
            )

            knowledge_graph.add_node(
                profession
            )

            imported += 1

        return imported
    # ----------------------------------------------------------------
    # SKILLS
    # ----------------------------------------------------------------

    def import_skills(
        self,
        rows: list[dict]
    ) -> int:

        imported = 0

        for row in rows:

            skill_id = str(

                row.get("conceptUri")
                or row.get("id")
                or row.get("uri")
                or ""

            ).strip()

            skill_name = (

                row.get("preferredLabel")
                or row.get("title")
                or row.get("name")
                or ""

            ).strip()

            if not skill_id:

                continue

            if not skill_name:

                continue

            if skill_repository.get(
                skill_id
            ):
                continue

            description = row.get(
                "description",
                ""
            )

            skill_type = (

                row.get("skillType")
                or row.get("type")
                or row.get("category")
                or "ESCO"

            )

            skill = Skill(

                id=skill_id,

                name=skill_name,

                category=skill_type,

                description=description

            )

            skill_repository.add(
                skill
            )

            knowledge_graph.add_node(
                skill
            )

            imported += 1

        return imported

    # ----------------------------------------------------------------
    # RELATIONS
    # ----------------------------------------------------------------

    def import_relations(
        self,
        rows: list[dict]
    ) -> int:

        imported = 0

        for row in rows:

            source = str(

                row.get("occupation")
                or row.get("occupationUri")
                or row.get("source")
                or ""

            ).strip()

            target = str(

                row.get("skill")
                or row.get("skillUri")
                or row.get("target")
                or ""

            ).strip()

            if not source:

                continue

            if not target:

                continue

            relation = (

                row.get("relation")
                or row.get("relationType")
                or "HAS_SKILL"

            )

            weight = float(

                row.get(

                    "weight",

                    1

                )

            )

            edge = KnowledgeEdge(

                source=source,

                target=target,

                relation=relation,

                weight=weight

            )

            knowledge_graph.add_edge(
                edge
            )

            imported += 1

        return imported
    # ----------------------------------------------------------------
    # GRAPH VALIDATION
    # ----------------------------------------------------------------

    def validate_graph(self) -> dict:
        """
        Validate graph consistency after import.
        """

        report = {

            "missing_professions": [],

            "missing_skills": [],

            "orphan_edges": 0

        }

        for edge in knowledge_graph.edges:

            if not knowledge_graph.has_node(edge.source):

                report["missing_professions"].append(
                    edge.source
                )

                report["orphan_edges"] += 1

            if not knowledge_graph.has_node(edge.target):

                report["missing_skills"].append(
                    edge.target
                )

                report["orphan_edges"] += 1

        report["missing_professions"] = sorted(
            list(
                set(
                    report["missing_professions"]
                )
            )
        )

        report["missing_skills"] = sorted(
            list(
                set(
                    report["missing_skills"]
                )
            )
        )

        return report

    # ----------------------------------------------------------------
    # IMPORT MULTIPLE FILES
    # ----------------------------------------------------------------

    def import_directory(self) -> dict:

        stats = {

            "occupations": 0,

            "skills": 0,

            "relations": 0

        }

        if self.exists("occupations.csv"):

            stats["occupations"] = self.import_occupations(

                self.csv("occupations.csv")

            )

        if self.exists("skills.csv"):

            stats["skills"] = self.import_skills(

                self.csv("skills.csv")

            )

        if self.exists("relations.csv"):

            stats["relations"] = self.import_relations(

                self.csv("relations.csv")

            )

        return stats

    # ----------------------------------------------------------------
    # DASHBOARD
    # ----------------------------------------------------------------

    def statistics(self):

        graph = knowledge_graph.statistics()

        return {

            "professions":

                profession_repository.count(),

            "skills":

                skill_repository.count(),

            "graph":

                graph

        }

    # ----------------------------------------------------------------

    def report(self):

        return {

            "statistics":

                self.statistics(),

            "validation":

                self.validate_graph()

        }

        # ----------------------------------------------------------------
        # IMPORT ALL
        # ----------------------------------------------------------------

        def import_all(self) -> dict:
            """
            Complete ESCO import.

            Imports every supported dataset
            found inside datasets/esco/.
            """

            statistics = {

                "occupations": 0,

                "skills": 0,

                "relations": 0,

                "additional_relations": 0

            }

            #
            # Occupations
            #

            if self.exists("occupations.csv"):
                statistics["occupations"] = (

                    self.import_occupations(

                        self.csv("occupations.csv")

                    )

                )

            #
            # Skills
            #

            if self.exists("skills.csv"):
                statistics["skills"] = (

                    self.import_skills(

                        self.csv("skills.csv")

                    )

                )

            #
            # Main Relations
            #

            if self.exists("relations.csv"):
                statistics["relations"] = (

                    self.import_relations(

                        self.csv("relations.csv")

                    )

                )

            #
            # Optional ESCO relation files
            #

            optional_relation_files = [

                "occupationSkillRelations.csv",

                "occupationSkillRelation.csv",

                "occupation_skills.csv",

                "occupation_skill_relations.csv",

                "skillHierarchy.csv",

                "skill_hierarchy.csv",

                "broaderRelations.csv",

                "broader_relations.csv",

                "narrowerRelations.csv",

                "narrower_relations.csv"

            ]

            for filename in optional_relation_files:

                if not self.exists(filename):
                    continue

                statistics["additional_relations"] += (

                    self.import_relations(

                        self.csv(filename)

                    )

                )

            #
            # Final Report
            #

            statistics["graph"] = knowledge_graph.statistics()

            statistics["validation"] = self.validate_graph()

            return statistics

        # ----------------------------------------------------------------

        def clear(self):
            """
            Clears repositories before
            complete reimport.
            """

            profession_repository.clear()

            skill_repository.clear()

            knowledge_graph.clear()

        # ----------------------------------------------------------------

        def rebuild(self):

            """
            Full rebuild.

            Clears graph

            Imports datasets

            Returns report
            """

            self.clear()

            return self.import_all()

        # ----------------------------------------------------------------

        def __repr__(self):

            return (

                "<ESCOImporter "

                f"path='{self.root}'>"

            )

    # ================================================================
    # GLOBAL SINGLETON
    # ================================================================

    esco_importer = ESCOImporter(

        "datasets/esco"

    )