"""
Workspace Manager
"""

from .loader import load


class WorkspaceManager:

    workspace=None


    @classmethod

    def initialize(cls):

        cls.workspace=load()

        return cls.workspace