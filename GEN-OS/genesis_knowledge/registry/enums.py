"""
════════════════════════════════════════════════════════════════════
GENESIS HR®
Knowledge Core

Module:Entity Registry
File:enums.py
Purpose:Global enumerations used across the Knowledge Core.
Author:Genesis Engineering Team
════════════════════════════════════════════════════════════════════
"""

from enum import Enum


class EntityType(str, Enum):
    PROFESSION = "profession"
    COMPETENCY = "competency"
    ARCHETYPE = "archetype"
    SKILL = "skill"
    HABIT = "habit"
    SPORT = "sport"
    BOOK = "book"
    COURSE = "course"
    UNIVERSITY = "university"
    CERTIFICATION = "certification"
    PROJECT = "project"
    INDUSTRY = "industry"
    TECHNOLOGY = "technology"
    TOOL = "tool"
    LANGUAGE = "language"
    COMPANY = "company"
    ROLE = "role"
    TASK = "task"
    PROTOCOL = "protocol"
    ENVIRONMENT = "environment"
    PERSONALITY_TRAIT = "personality_trait"
    VALUE = "value"
    INTEREST = "interest"
    HOBBY = "hobby"
    MARKET = "market"
    COUNTRY = "country"
    CITY = "city"
    SALARY = "salary"
    EDUCATION = "education"
    OTHER = "other"


class EntityStatus(str, Enum):
    DRAFT = "draft"
    IMPORTED = "imported"
    VERIFIED = "verified"
    ENRICHED = "enriched"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class EntitySource(str, Enum):
    MANUAL = "manual"
    EXCEL = "excel"
    CSV = "csv"
    JSON = "json"
    API = "api"
    ESCO = "esco"
    ONET = "onet"
    AI = "ai"
    WIKIPEDIA = "wikipedia"
    INTERNAL = "internal"


class ConfidenceLevel(str, Enum):
    UNKNOWN = "unknown"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERIFIED = "verified"
