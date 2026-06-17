from models import (
    db,
    Competency
)
from core.competency_registry import (
    COMPETENCY_REGISTRY
)


def seed_competencies():
    created = 0
    for category, items in (
            COMPETENCY_REGISTRY.items()
    ):
        for title in items:
            code = (
                title
                .lower()
                .replace(" ", "_")
            )
            exists = (
                Competency.query
                .filter_by(
                    code=code
                )
                .first()
            )
            if exists:
                continue
            competency = Competency(
                code=code,
                title=title,
                category=category
            )
            db.session.add(
                competency
            )
            created += 1
    db.session.commit()
    return created
