"""
═══════════════════════════════════════════════════════════════════════

MODULE ID:     GKH-SCHEMA-001
NAME:     Genesis Knowledge Schema
LAYER:     Knowledge Core
VERSION:     0.1.0 Alpha
STATUS:     Stable
DESCRIPTION
Single source of truth describing every
knowledge object inside Genesis.

This file contains:
• Entity Types
• Relation Types
• Source Types
• Status Types
• Confidence Levels

Every module in Genesis MUST import
definitions only from here.
═══════════════════════════════════════════════════════════════════════
"""

from enum import Enum


# ===========================================================
# ENTITY TYPES
# ===========================================================

class EntityType(str, Enum):
    PROFESSION = "profession"
    COMPETENCY = "competency"
    SKILL = "skill"
    HABIT = "habit"
    HOBBY = "hobby"
    SPORT = "sport"
    BOOK = "book"
    COURSE = "course"
    PROTOCOL = "protocol"
    ENVIRONMENT = "environment"
    BEHAVIOR = "behavior"
    TRAIT = "trait"
    VALUE = "value"
    GOAL = "goal"
    TECHNOLOGY = "technology"
    SOFTWARE = "software"
    TOOL = "tool"
    LANGUAGE = "language"
    EDUCATION = "education"
    DEGREE = "degree"
    CERTIFICATION = "certification"
    PERSONALITY = "personality"
    ARCHETYPE = "archetype"
    EMOTION = "emotion"
    RISK = "risk"
    COMPANY = "company"
    INDUSTRY = "industry"
    PROJECT = "project"
    METHODOLOGY = "methodology"
    FRAMEWORK = "framework"
    MINDSET = "mindset"
    LIFESTYLE = "lifestyle"
    COMMUNITY = "community"


# ===========================================================
# RELATION TYPES
# ===========================================================

class RelationType(str, Enum):
    REQUIRES = "requires"
    DEVELOPS = "develops"
    IMPROVES = "improves"
    WEAKENS = "weakens"
    SUPPORTS = "supports"
    BLOCKS = "blocks"
    REDUCES = "reduces"
    INCREASES = "increases"
    TEACHES = "teaches"
    LEARNS = "learns"
    RECOMMENDS = "recommends"
    BELONGS_TO = "belongs_to"
    PART_OF = "part_of"
    LEADS_TO = "leads_to"
    NEXT_STEP = "next_step"
    PREVIOUS_STEP = "previous_step"
    SIMILAR_TO = "similar_to"
    OPPOSITE_TO = "opposite_to"
    USES = "uses"
    CREATES = "creates"
    DEPENDS_ON = "depends_on"
    GOOD_FOR = "good_for"
    BAD_FOR = "bad_for"
    STRENGTHENS = "strengthens"
    INFLUENCES = "influences"
    PREDICTS = "predicts"
    CAUSES = "causes"
    ENABLES = "enables"
    COMPATIBLE_WITH = "compatible_with"
    INCOMPATIBLE_WITH = "incompatible_with"


# ===========================================================
# DATA SOURCES
# ===========================================================

class SourceType(str, Enum):
    MANUAL = "manual"
    EXCEL = "excel"
    CSV = "csv"
    JSON = "json"
    ESCO = "esco"
    ONET = "onet"
    WIKIDATA = "wikidata"
    WIKIPEDIA = "wikipedia"
    OPEN_LIBRARY = "openlibrary"
    GOOGLE_BOOKS = "google_books"
    AI = "ai"
    USER = "user"


# ===========================================================
# ENTITY STATUS
# ===========================================================

class EntityStatus(str, Enum):
    DRAFT = "draft"
    IMPORTED = "imported"
    VERIFIED = "verified"
    CURATED = "curated"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"


# ===========================================================
# CONFIDENCE LEVEL
# ===========================================================

class ConfidenceLevel(float, Enum):
    VERY_LOW = 0.2
    LOW = 0.4
    MEDIUM = 0.6
    HIGH = 0.8
    VERIFIED = 1.0
