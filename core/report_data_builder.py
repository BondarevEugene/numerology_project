class ReportDataBuilder:

    @staticmethod
    def build(
        matrix,
        destiny_number,
        archetype,
        adv_results,
        jobs,
        cell_statuses
    ):
        return {
            "number": destiny_number,
            "title": archetype.get(
                "title",
                "Анализ"
            ),
            "interpretation": archetype.get(
                "interpretation",
                ""
            ),
            "planet": archetype.get(
                "planet",
                "—"
            ),
            "element": archetype.get(
                "element",
                "—"
            ),
            "jobs": jobs,
            "advanced": adv_results,
            **cell_statuses,
            "m1": matrix.get("1", ""),
            "m2": matrix.get("2", ""),
            "m3": matrix.get("3", ""),
            "m4": matrix.get("4", ""),
            "m5": matrix.get("5", ""),
            "m6": matrix.get("6", ""),
            "m7": matrix.get("7", ""),
            "m8": matrix.get("8", ""),
            "m9": matrix.get("9", "")
        }