import maya.cmds as mc
import maya.mel as mm


def print(text):
    """
    Print given text in mel so that is visible in Maya's log bar
    
    Args:
        text (str): the text to print
    """
    mm.eval(f'print "{text}"')
    
    return


'''                   '''
''' CREATE ATTRIBUTES '''
'''                   '''

def addBool(attr, obj, value=False, keyable=True, locked=False, channelbox=True):
    """
    Add a boolean attribute to given object

    Args:
        attr (str): attribute name
        obj (str): object to add the attribute
        value (bool, optional): default value. Defaults to False.
        keyable (bool, optional): should the new attribute be keyable? Defaults to True.
        locked (bool, optional): should the new attribute be locked? Defaults to False.
        channelbox (bool, optional): should the new attribute be displayed in the channel box? Defaults to True.

    Returns:
        str: full attribute name
    """
    
    attr = attr.replace(' ','_')
    ret = f"{obj}.{attr}"
    
    # IF ATTRIBUTE ALREADY EXISTS, RETURN FULL NAME
    if mc.objExists(ret):
        return ret
    
    # ADD ATTRIBUTE
    mc.addAttr(obj, ln=attr, at='bool', dv=value)

    # SETTINGS
    mc.setAttr(ret, value)
    mc.setAttr(ret , e=1, k=keyable)
    mc.setAttr(ret , e=1, l=locked)
    mc.setAttr(ret , e=1, cb=channelbox)    
           
    return ret


def addFloat(attr, obj, value=0, min=None, max=None, keyable=True, locked=False, channelbox=True):
    """
    Add a float attribute to given object

    Args:
        attr (str): attribute name
        obj (str): object to add the attribute
        value (float, optional): default value. Defaults to 0.
        min (float, optional): minimum value. Defaults to None.
        max (float, optional): maximum value. Defaults to None.
        keyable (bool, optional): should the new attribute be keyable? Defaults to True.
        locked (bool, optional): should the new attribute be locked? Defaults to False.
        channelbox (bool, optional): should the new attribute be displayed in the channel box? Defaults to True.

    Returns:
        str: full attribute name
    """
        
    attr = attr.replace(' ','_')
    ret = f"{obj}.{attr}"
    
    # IF ATTRIBUTE ALREADY EXISTS, RETURN FULL NAME
    if mc.objExists(ret):
        return ret
    
    # ADD ATTRIBUTE AND SET min AND max
    mc.addAttr(obj, ln=attr, at='double', dv=value)
    if min:
        mc.addAttr(ret, e=True, min=min)
    if max:
        mc.addAttr(ret, e=True, max=max)

    # SETTINGS
    mc.setAttr(ret, value)
    mc.setAttr(ret , e=1, k=keyable)
    mc.setAttr(ret , e=1, l=locked)
    mc.setAttr(ret , e=1, cb=channelbox)
            
    return ret


def addInt(attr, obj, value=0, min=None, max=None, keyable=True, locked=False, channelbox=True):
    """
    Add an int attribute to given object

    Args:
        attr (str): attribute name
        obj (str): object to add the attribute
        value (int, optional): default value. Defaults to 0.
        min (int, optional): minimum value. Defaults to None.
        max (int, optional): maximum value. Defaults to None.
        keyable (bool, optional): should the new attribute be keyable? Defaults to True.
        locked (bool, optional): should the new attribute be locked? Defaults to False.
        channelbox (bool, optional): should the new attribute be displayed in the channel box? Defaults to True.

    Returns:
        str: full attribute name
    """
    
    attr = attr.replace(' ','_')
    ret = f"{obj}.{attr}"
    
    # IF ATTRIBUTE ALREADY EXISTS, RETURN FULL NAME
    if mc.objExists(ret):
        return ret
    
    # ADD ATTRIBUTE AND SET min AND max
    mc.addAttr(obj, ln=attr, at='long', dv=value)
    if min:
        mc.addAttr(ret, e=True, min=min)
    if max:
        mc.addAttr(ret, e=True, max=max)

    # SETTINGS
    mc.setAttr(ret, value)
    mc.setAttr(ret , e=1, k=keyable)
    mc.setAttr(ret , e=1, l=locked)
    mc.setAttr(ret , e=1, cb=channelbox)
    
    return ret


def addString(attr, obj, value='', keyable=True, locked=False, channelbox=True):
    """
    Add a string attribute to given object

    Args:
        attr (str): attribute name
        obj (str): object to add the attribute
        value (str, optional): default value. Defaults to "".
        keyable (bool, optional): should the new attribute be keyable? Defaults to True.
        locked (bool, optional): should the new attribute be locked? Defaults to False.
        channelbox (bool, optional): should the new attribute be displayed in the channel box? Defaults to True.

    Returns:
        str: full attribute name
    """
    
    attr = attr.replace(' ','_')
    ret = f"{obj}.{attr}"
    
    # IF ATTRIBUTE ALREADY EXISTS, RETURN FULL NAME
    if mc.objExists(ret):
        return ret
    
    # ADD ATTRIBUTE
    mc.addAttr(obj, ln=attr, dt='string')

    # SETTINGS
    mc.setAttr(ret, value, type="string")
    mc.setAttr(ret , e=1, k=keyable)
    mc.setAttr(ret , e=1, l=locked)
    mc.setAttr(ret , e=1, cb=channelbox)

    return ret


def addEnum(attr, obj, cases, value=0, keyable=True, locked=False, channelbox=True):
    """
    Add an enum attribute to given object

    Args:
        attr (str): attribute name
        obj (str): object to add the attribute
        cases (str, list): the available options. Could be either a string "item1:item2:item3" or a list ["item1", "item2", "item3"]
        value (int, optional): default value. Defaults to 0.
        keyable (bool, optional): should the new attribute be keyable? Defaults to True.
        locked (bool, optional): should the new attribute be locked? Defaults to False.
        channelbox (bool, optional): should the new attribute be displayed in the channel box? Defaults to True.

    Returns:
        str: full attribute name
    """
    
    attr = attr.replace(' ','_')
    ret = f"{obj}.{attr}"
    
    # IF ATTRIBUTE ALREADY EXISTS, RETURN FULL NAME
    if mc.objExists(ret):
        return ret
    
    # CONVERT CASES TO VALID STRING
    if isinstance(cases, list):
        cases = ":".join(cases)
    
    # ADD ATTRIBUTE
    mc.addAttr(obj, ln=attr, at='enum', dv=value, en=cases)

    # SETTING
    mc.setAttr(ret, value)
    mc.setAttr(ret , e=1, k=keyable)
    mc.setAttr(ret , e=1, l=locked)
    mc.setAttr(ret , e=1, cb=channelbox)
        
    return ret


def addVector(attr, obj, keyable=True, locked=False, channelbox=True):
    """
    Add a vector attribute to given object

    Args:
        attr (str): attribute name
        obj (str): object to add the attribute
        keyable (bool, optional): should the new attribute be keyable? Defaults to True.
        locked (bool, optional): should the new attribute be locked? Defaults to False.
        channelbox (bool, optional): should the new attribute be displayed in the channel box? Defaults to True.

    Returns:
        str: full attribute name
    """
    
    attr = attr.replace(' ','_')
    ret = f"{obj}.{attr}"
    
    # IF ATTRIBUTE ALREADY EXISTS, RETURN FULL NAME
    if mc.objExists(ret):
        return ret
    
    # ADD ATTRIBUTE
    mc.addAttr(obj ,ln=attr, at='double3')
    for ax in "XYZ" :
        mc.addAttr(obj, ln=attr+ax, at='double', p=attr)

    # SETTINGS
    for ax in "_XYZ":
        mc.setAttr(ret+ax.replace("_", ""), e=1, k=keyable)
        mc.setAttr(ret+ax.replace("_", ""), e=1, l=locked)
        mc.setAttr(ret+ax.replace("_", ""), e=1, cb=channelbox)
    
    return ret


def addDivider(title, obj):
    """
    Add a divider attribute to given object

    Args:
        title (str): divider label
        obj (str): object to add the divider to
    """
    
    if not mc.objExists(f"{obj}.{title}"):
        addEnum(title, obj, '_________', keyable=False, locked=True, channelbox=True)

    return

addSeparator = addDivider


'''                    '''
''' SESSION MANAGEMENT '''
'''                    '''

def geppettoExists():
    """
    Check if a session exists in the database

    Returns:
        bool: True if "rig" group exists, False if it doesn't
    """
    if mc.objExists("geppetto"):
        return True
    
    return False


def createBaseStructure():
    """
    Create base groups structure to initialize Geppetto
    """
    
    # CREATE AND PARENT GROUPS
    geppetto = mc.group(n="geppetto", em=True)
    modules = mc.group(n="modules", em=True)
    blueprints = mc.group(n="blueprints", em=True)
    mc.parent(modules, blueprints, geppetto)
    
    # CREATE MAIN ATTRIBUTES
    addString("session_path", geppetto, keyable=False, channelbox=False)
    addString("rig_name", geppetto, keyable=False, channelbox=False)
    addString("publish_path", geppetto, keyable=False, channelbox=False)

    return


def getGeppetto():
    ret = mc.ls("geppetto", l=True)
    if ret:
        return ret[0]
    
    mc.error("Couldn't find Geppetto. Maybe he's out for lunch.")
    return None


def getModules():
    root = getGeppetto()
    ret = mc.listRelatives(f"{root}|modules")
    if ret:
        return ret
    return []