"""
═══════════════════════════════════════════════════════════════════════
MODULE ID:    GKH-PIPE-003
NAME:    Universal Pipeline
DESCRIPTION
Executes every registered Stage.
═══════════════════════════════════════════════════════════════════════
"""

from .pipeline_context import PipelineContext


class Pipeline:

    def __init__(self):
        self.stages = []

    def add_stage(self, stage):
        self.stages.append(stage)

    def run(self, context=None):
        if context is None:
            context = PipelineContext()
        print("🚀 Genesis Pipeline started")
        for stage in self.stages:
            print(f"⚙ {stage.__class__.__name__}")
            stage.execute(context)
        print("✅ Pipeline completed")
        return context
