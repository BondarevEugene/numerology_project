"""
GENOS Window
"""

from dataclasses import dataclass


@dataclass
class Window:

    id:str

    title:str

    component:str

    icon:str="□"

    width:int=500

    height:int=400

    visible:bool=True

    dock:str="center"

    minimizable:bool=True

    closable:bool=True

    resizable:bool=True