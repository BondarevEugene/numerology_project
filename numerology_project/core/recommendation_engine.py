from core.archetype_matrix import (
    ARCHETYPE_MATRIX
)

from models import (
    Profession,
    ProfessionCompetency
)


class RecommendationEngine:

    @staticmethod
    def calculate_match(
        archetype_number,
        profession_id
    ):

        archetype_vector = (
            ARCHETYPE_MATRIX.get(
                archetype_number,
                {}
            )
        )

        profession_links = (
            ProfessionCompetency
            .query
            .filter_by(
                profession_id=profession_id
            )
            .all()
        )

        if not profession_links:

            return {
                "score": 0,
                "matches": [],
                "gaps": []
            }

        total = 0

        count = 0

        matches = []

        gaps = []

        for link in profession_links:

            competency_code = (
                link
                .competency
                .code
            )

            profession_weight = (
                link.weight
            )

            archetype_weight = (
                archetype_vector.get(
                    competency_code,
                    50
                )
            )

            diff = abs(
                archetype_weight -
                profession_weight
            )

            score = (
                100 - diff
            )

            total += score

            count += 1

            item = {

                "competency":
                    competency_code,

                "archetype":
                    archetype_weight,

                "profession":
                    profession_weight,

                "score":
                    score
            }

            if score >= 80:

                matches.append(
                    item
                )

            if score <= 55:

                gaps.append(
                    item
                )

        final_score = (
            round(
                total / count,
                1
            )
            if count
            else 0
        )

        return {

            "score":
                final_score,

            "matches":
                sorted(
                    matches,
                    key=lambda x:
                    x["score"],
                    reverse=True
                ),

            "gaps":
                sorted(
                    gaps,
                    key=lambda x:
                    x["score"]
                )
        }

    @staticmethod
    def find_best_professions(
            archetype_number
    ):

        professions = (
            Profession
            .query
            .filter_by(
                is_active=True
            )
            .all()
        )

        results = []

        for profession in professions:
            result = (
                RecommendationEngine
                .calculate_match(
                    archetype_number,
                    profession.id
                )
            )

            results.append({

                "profession":
                    profession,

                "score":
                    result["score"]
            })

        return sorted(
            results,
            key=lambda x:
            x["score"],
            reverse=True
        )