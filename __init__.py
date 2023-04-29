import maya.cmds as mc
import maya.mel as mm
import maya._OpenMaya as om
import maya.api.OpenMaya as om2

import importlib as imp

from .utils import toolbox as tb
from .ui import *

imp.reload(ui)
imp.reload(tb)


def start():
    # # CHECK IF SESSION EXISTS
    # if not tb.geppettoExists():
    #     tb.createBaseStructure()
    #     tb.print("Session created")
        
    # OPEN UI
    workshop = Workshop()
    workshop.start()
    
    return
