from . import skeleton_creation
from . import bone_operators
from . import controller_creation

def register():
    skeleton_creation.register()
    bone_operators.register()
    controller_creation.register()

def unregister():
    skeleton_creation.unregister()
    bone_operators.unregister()
    controller_creation.unregister()