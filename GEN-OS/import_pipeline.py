"""
===============================================================================

 GENESIS HR®
 GEN-OS

 FILE
 ----
 services/import_pipeline.py

 BUILD
 -----
 0.2.1

 DESCRIPTION
 -----------
 Complete Knowledge Import Pipeline.

 Responsibilities

    • Provider initialization

    • Dataset validation

    • Mapping

    • Graph building

    • Statistics

===============================================================================
"""

from __future__ import annotations

import logging

from pathlib import Path

from providers.esco_provider import ESCOProvider
from providers.onet_provider import ONETProvider

from mappers.profession_mapper import ProfessionMapper
from mappers.skill_mapper import SkillMapper
from mappers.relation_mapper import RelationMapper

from services.knowledge_graph_service import (
    knowledge_graph
)


LOGGER = logging.getLogger(
    "GEN-OS.ImportPipeline"
)


class ImportPipeline:
    """
    Complete import pipeline.

        ESCO

            +

        O*NET

            ↓

        Models

            ↓

        Graph

    """

    def __init__(
        self,
        datasets_root: Path
    ):

        self.datasets_root = Path(
            datasets_root
        )

        self.esco = ESCOProvider(

            self.datasets_root / "esco"

        )

        self.onet = ONETProvider(

            self.datasets_root / "onet"

        )

    # ------------------------------------------------------------

    def initialize(self):

        LOGGER.info(
            "Initializing providers..."
        )

        self.esco.initialize()

        self.onet.initialize()

        LOGGER.info(
            "Providers READY."
        )

    # ------------------------------------------------------------

    def clear(self):

        knowledge_graph.clear()

    # ------------------------------------------------------------

    def import_all(self):

        """
        Complete import.

        Returns statistics.
        """

        self.clear()

        self.initialize()

        result = {

            "providers": {},

            "graph": {}

        }

        result["providers"]["ESCO"] = (

            self.import_esco()

        )

        result["providers"]["ONET"] = (

            self.import_onet()

        )

        result["graph"] = (

            knowledge_graph.statistics()

        )

        return result
    # ------------------------------------------------------------------
    # ESCO IMPORT
    # ------------------------------------------------------------------

    def import_esco(self) -> dict:
        """
        Import complete ESCO dataset.
        """

        LOGGER.info(
            "Importing ESCO..."
        )

        professions = self._import_esco_professions()

        skills = self._import_esco_skills()

        relations = self._import_esco_relations()

        LOGGER.info(
            "ESCO imported."
        )

        return {

            "professions": professions,

            "skills": skills,

            "relations": relations

        }

    # ------------------------------------------------------------------

    def _import_esco_professions(self) -> int:

        count = 0

        for row in self.esco.professions():

            profession = ProfessionMapper.from_esco(
                row
            )

            profession = ProfessionMapper.normalize(
                profession
            )

            if not ProfessionMapper.validate(
                profession
            ):
                continue

            knowledge_graph.add_node(
                profession
            )

            count += 1

        LOGGER.info(
            "ESCO professions: %d",
            count
        )

        return count

    # ------------------------------------------------------------------

    def _import_esco_skills(self) -> int:

        count = 0

        for row in self.esco.skills():

            skill = SkillMapper.from_esco(
                row
            )

            skill = SkillMapper.normalize(
                skill
            )

            if not SkillMapper.validate(
                skill
            ):
                continue

            knowledge_graph.add_node(
                skill
            )

            count += 1

        LOGGER.info(
            "ESCO skills: %d",
            count
        )

        return count

    # ------------------------------------------------------------------

    def _import_esco_relations(self) -> int:

        count = 0

        for row in self.esco.relations():

            edge = RelationMapper.profession_skill(
                row
            )

            if not RelationMapper.validate(
                edge
            ):
                continue

            knowledge_graph.add_edge(
                edge
            )

            count += 1

        LOGGER.info(
            "ESCO relations: %d",
            count
        )

        return count
    # ------------------------------------------------------------------
    # O*NET IMPORT
    # ------------------------------------------------------------------

    def import_onet(self) -> dict:
        """
        Import complete O*NET dataset.
        """

        LOGGER.info(
            "Importing O*NET..."
        )

        professions = self._import_onet_professions()

        skills = self._import_onet_skills()

        LOGGER.info(
            "O*NET imported."
        )

        return {

            "professions": professions,

            "skills": skills

        }

    # ------------------------------------------------------------------

    def _import_onet_professions(self) -> int:

        imported = 0

        for row in self.onet.occupations():

            profession = ProfessionMapper.from_onet(
                row
            )

            profession = ProfessionMapper.normalize(
                profession
            )

            if not ProfessionMapper.validate(
                profession
            ):
                continue

            if knowledge_graph.has_node(
                profession.id
            ):

                existing = knowledge_graph.node(
                    profession.id
                )

                ProfessionMapper.merge(
                    existing,
                    profession
                )

            else:

                knowledge_graph.add_node(
                    profession
                )

            imported += 1

        LOGGER.info(

            "Imported O*NET professions: %d",

            imported

        )

        return imported

    # ------------------------------------------------------------------

    def _import_onet_skills(self) -> int:

        imported = 0

        for row in self.onet.skills():

            skill = SkillMapper.from_onet(
                row
            )

            skill = SkillMapper.normalize(
                skill
            )

            if not SkillMapper.validate(
                skill
            ):
                continue

            if knowledge_graph.has_node(
                skill.id
            ):

                existing = knowledge_graph.node(
                    skill.id
                )

                SkillMapper.merge(
                    existing,
                    skill
                )

            else:

                knowledge_graph.add_node(
                    skill
                )

            imported += 1

        LOGGER.info(

            "Imported O*NET skills: %d",

            imported

        )

        return imported

    # ------------------------------------------------------------------

    def graph(self):

        """
        Return current graph.
        """

        return knowledge_graph

        # ------------------------------------------------------------------
        # VALIDATION
        # ------------------------------------------------------------------

        def validate(self) -> dict:
            """
            Validate providers before import.
            """

            report = {

                "esco": self.esco.validate(),

                "onet": self.onet.validate()

            }

            report["ok"] = all(
                report.values()
            )

            return report

        # ------------------------------------------------------------------
        # SUMMARY
        # ------------------------------------------------------------------

        def summary(self) -> dict:
            """
            Pipeline summary.
            """

            graph_stats = knowledge_graph.statistics()

            return {

                "providers": {

                    "ESCO": self.esco.metadata(),

                    "ONET": self.onet.metadata()

                },

                "graph": graph_stats

            }

        # ------------------------------------------------------------------
        # EXPORT
        # ------------------------------------------------------------------

        def export_json(
                self,
                output: Path
        ) -> Path:
            """
            Export graph to JSON.
            """

            import json

            output.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            output.write_text(

                json.dumps(

                    knowledge_graph.export_json(),

                    indent=4,

                    ensure_ascii=False

                ),

                encoding="utf-8"

            )

            LOGGER.info(

                "Knowledge graph exported: %s",

                output

            )

            return output

        # ------------------------------------------------------------------
        # RESET
        # ------------------------------------------------------------------

        def reset(self) -> None:
            """
            Clear runtime graph.
            """

            LOGGER.info(
                "Resetting pipeline..."
            )

            knowledge_graph.clear()

        # ------------------------------------------------------------------
        # STATUS
        # ------------------------------------------------------------------

        def status(self) -> dict:
            """
            Runtime status.
            """

            validation = self.validate()

            return {

                "datasets_root": str(
                    self.datasets_root
                ),

                "validation": validation,

                "graph": knowledge_graph.statistics()

            }

        # ------------------------------------------------------------------

        def run(self) -> dict:
            """
            Complete pipeline execution.

                Validate

                    ↓

                Import

                    ↓

                Summary

            """

            LOGGER.info(
                "=" * 70
            )

            LOGGER.info(
                "GEN-OS IMPORT PIPELINE"
            )

            LOGGER.info(
                "=" * 70
            )

            validation = self.validate()

            if not validation["ok"]:
                raise RuntimeError(

                    "Dataset validation failed."

                )

            result = self.import_all()

            LOGGER.info(
                "Import finished."
            )

            LOGGER.info(

                "Nodes: %d",

                knowledge_graph.node_count()

            )

            LOGGER.info(

                "Edges: %d",

                knowledge_graph.edge_count()

            )

            return result

    # ==============================================================================
    # FACTORY
    # ==============================================================================

    _pipeline: ImportPipeline | None = None

    def create_pipeline(
            datasets_root: Path
    ) -> ImportPipeline:

        global _pipeline

        if _pipeline is None:
            _pipeline = ImportPipeline(
                datasets_root
            )

        return _pipeline