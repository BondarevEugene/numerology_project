"""
═══════════════════════════════════════════════════════════════════════

MODULE ID:     GKH-PIPE-001
NAME:     Pipeline Context
DESCRIPTION
Shared object travelling through
every Pipeline Stage.
Each stage modifies Context.
Nothing is returned.

═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass, field


@dataclass
class PipelineContext:
    provider: str = ""
    source: str = ""
    raw_data: list = field(default_factory=list)
    entities: list = field(default_factory=list)
    relations: list = field(default_factory=list)
    statistics: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    logs: list = field(default_factory=list)
