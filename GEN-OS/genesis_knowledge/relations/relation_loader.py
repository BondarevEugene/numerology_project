"""
GENESIS HR®

Relation Loader
"""

import json

from pathlib import Path

from .relation_factory import RelationFactory


class RelationLoader:

    @staticmethod
    def load(path):

        path = Path(path)

        data = json.loads(

            path.read_text(

                encoding="utf-8"

            )

        )

        return RelationFactory.create(

            source=data["source"],

            target=data["target"],

            relation_type=data["relation_type"],

            weight=data.get(

                "weight",

                1.0

            ),

            confidence=data.get(

                "confidence",

                1.0

            ),

            metadata=data.get(

                "metadata",

                {}

            )

        )