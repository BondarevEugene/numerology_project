"""
Window Registry
"""

from .window import Window


WINDOWS={}


def register(window:Window):

    WINDOWS[window.id]=window


def get(window_id):

    return WINDOWS.get(window_id)


def all():

    return WINDOWS.values()