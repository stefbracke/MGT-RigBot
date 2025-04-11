from . import skeleton
from . import bone
from . import pose
from . import skinning
from . import constraint

def register():
    skeleton.register()
    bone.register()
    pose.register()
    skinning.register()
    constraint.register()

def unregister():
    constraint.unregister()
    skinning.unregister()
    pose.unregister()
    bone.unregister()
    skeleton.unregister()
