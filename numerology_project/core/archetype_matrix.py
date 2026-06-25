from core.archetype_profiles import ARCHETYPE_PROFILES

COMPETENCIES = [
    "leadership",
    "influence",
    "decision_making",
    "responsibility",
    "authority",

    "strategy",
    "system_thinking",
    "planning",
    "risk_management",
    "vision",

    "analysis",
    "critical_thinking",
    "research",
    "problem_solving",
    "logic",

    "communication",
    "negotiation",
    "persuasion",
    "teaching",
    "presentation",

    "execution",
    "discipline",
    "consistency",
    "organization",
    "time_management",

    "adaptability",
    "learning_agility",
    "stress_tolerance",
    "flexibility",
    "resilience",

    "creativity",
    "innovation",
    "curiosity",
    "imagination",
    "experimentation",

    "empathy",
    "emotional_intelligence",
    "cooperation",
    "mentoring",
    "conflict_resolution"
]


def build_matrix():

    matrix = {}

    for archetype, profile in ARCHETYPE_PROFILES.items():

        matrix[archetype] = {}

        for competency in COMPETENCIES:

            matrix[archetype][competency] = 55

        for competency in profile["primary"]:

            matrix[archetype][competency] = 90

        for competency in profile["secondary"]:

            matrix[archetype][competency] = 75

        for competency in profile["low"]:

            matrix[archetype][competency] = 35

    return matrix


ARCHETYPE_MATRIX = build_matrix()