"""
==========================================================
GENESIS HR®
Knowledge Graph
Relation Types
Version: 1.0
==========================================================
"""

from enum import Enum


class RelationType(Enum):
    REQUIRES = "requires"
    DEVELOPS = "develops"
    IMPROVES = "improves"
    REDUCES = "reduces"
    RECOMMENDS = "recommends"
    RECOMMENDED_BOOK = "recommended_book"
    RECOMMENDED_COURSE = "recommended_course"
    RECOMMENDED_HOBBY = "recommended_hobby"
    RECOMMENDED_SPORT = "recommended_sport"
    LEADS_TO = "leads_to"
    PART_OF = "part_of"
    PARENT = "parent"
    CHILD = "child"
    SIMILAR = "similar"
    OPPOSITE = "opposite"
    NEXT_LEVEL = "next_level"
    PREVIOUS_LEVEL = "previous_level"
    BELONGS_TO = "belongs_to"
