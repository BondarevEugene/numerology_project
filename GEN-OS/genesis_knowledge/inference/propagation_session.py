"""
═══════════════════════════════════════════════════════════════
GENESIS HR®

Propagation Session
═══════════════════════════════════════════════════════════════
"""

import uuid
from datetime import datetime


class PropagationSession:

    def __init__(self):

        self.id=str(uuid.uuid4())

        self.started=datetime.utcnow()

        self.finished=None

    def finish(self):

        self.finished=datetime.utcnow()