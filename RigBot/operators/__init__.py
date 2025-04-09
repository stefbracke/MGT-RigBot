from . import skeleton
from . import bone
from . import pose

def register():
    skeleton.register()
    bone.register()
    pose.register()

def unregister():
    pose.unregister()
    bone.unregister()
    skeleton.unregister()
