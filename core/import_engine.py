from core.profession_importer import (
    ProfessionImporter
)


class ImportEngine:

    @staticmethod
    def run(

        import_type,
        path
    ):

        if import_type == "profession":

            return (
                ProfessionImporter
                .import_excel(
                    path
                )
            )

        raise Exception(
            "Unknown import type"
        )