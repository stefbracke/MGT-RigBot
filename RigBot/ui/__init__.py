from . import rigbot_panel
# from . import bone_list
# from . import controller_panel
# from . import viewport_panel
# from . import skeleton_panel

def register():
    rigbot_panel.register()
    # skeleton_panel.register()
    # controller_panel.register()
    # bone_list.register()
    # viewport_panel.register()

def unregister():
    rigbot_panel.unregister()
    # skeleton_panel.unregister()
    # controller_panel.unregister()
    # bone_list.unregister()
    # viewport_panel.unregister()