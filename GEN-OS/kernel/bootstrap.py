"""
═══════════════════════════════════════════════════════════════════════
GENESIS HR®
Kernel Bootstrap
═══════════════════════════════════════════════════════════════════════
"""

from kernel.kernel import kernel
from runtime.workspace_runtime import (
    workspace_runtime
)


def boot():
    workspace_runtime.boot()
    return kernel
