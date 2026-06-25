"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®

GEN-OS

Environment Service

BUILD:0053

DESCRIPTION

Работа со средами развития.

Environment = окружение,
в котором развивается человек.

═══════════════════════════════════════════════════════════════════════
"""


class EnvironmentService:

    def __init__(self):

        self.registry = None

    def attach(
        self,
        registry
    ):

        self.registry = registry

    def all(self):

        if self.registry is None:
            return []

        return self.registry.all()

    def count(self):

        return len(
            self.all()
        )

    def find(
        self,
        entity_id
    ):

        if self.registry is None:
            return None

        return self.registry.find(
            entity_id
        )

    def search(
        self,
        text
    ):

        result = []

        text = text.lower()

        for environment in self.all():

            title = getattr(
                environment,
                "title",
                ""
            )

            if text in title.lower():

                result.append(
                    environment
                )

        return result

    def statistics(self):

        return {

            "count":
                self.count()

        }


environment_service = EnvironmentService()