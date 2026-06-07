from content import ARCHETYPES

try:
    from content import ARCHETYPE_EXTRAS
except ImportError:
    ARCHETYPE_EXTRAS = {}


class ArchetypeService:
    @staticmethod
    def get(number: str):
        content_data = ARCHETYPES.get(
            number,
            {}
        )
        extra_data = ARCHETYPE_EXTRAS.get(
            number,
            {}
        )
        return {
            "title": content_data.get(
                "title",
                "Анализ"
            ),
            "interpretation": content_data.get(
                "full_text",
                ""
            ),
            "planet": extra_data.get(
                "planet",
                "—"
            ),
            "element": extra_data.get(
                "element",
                "—"
            ),
            "jobs": extra_data.get(
                "jobs",
                []
            ),
            "keywords": extra_data.get(
                "keywords",
                ""
            ),
            "description": extra_data.get(
                "description",
                ""
            ),
            "short_desc": content_data.get(
                "short_desc",
                ""
            ),

            "html_display": content_data.get(
                "html_display",
                ""
            )
        }