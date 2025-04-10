from . import skeleton
from . import bone
from . import pose
from . import skinning
from . import armature
from . import constraint

def register():
    skeleton.register()
    bone.register()
    pose.register()
    skinning.register()
    armature.register()
    constraint.register()

def unregister():
    constraint.unregister()
    armature.unregister()
    skinning.unregister()
    pose.unregister()
    bone.unregister()
    skeleton.unregister()
