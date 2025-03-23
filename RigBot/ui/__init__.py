from . import rigbot_panel
from . import viewport_panel

def register():
    rigbot_panel.register()
    viewport_panel.register()

def unregister():
    rigbot_panel.unregister()
    viewport_panel.unregister()