from . import skeleton_creation
from . import bone_operators

def register():
    skeleton_creation.register()
    bone_operators.register()

def unregister():
    skeleton_creation.unregister()
    bone_operators.unregister()