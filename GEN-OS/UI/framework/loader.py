"""
Workspace Loader
"""

from .workspace import Workspace

from .registry import all


def load():

    ws=Workspace(

        title="GENESIS"

    )

    for window in all():

        ws.add_window(

            window

        )

    return ws