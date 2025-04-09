from . import rigbot_panel
from . import viewport_panel
from . import pie_menu

def register():
    rigbot_panel.register()
    viewport_panel.register()
    pie_menu.register()

def unregister():
    rigbot_panel.unregister()
    viewport_panel.unregister()
    pie_menu.unregister()