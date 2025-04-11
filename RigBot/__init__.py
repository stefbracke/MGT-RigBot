import bpy

from . import operators
from . import ui

addon_keymaps = []

def register_keymaps():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon # Use addon keyconfig to avoid conflicts
    if not kc:
        print("Warning: Addon keyconfig not found.") # Should not happen usually
        return

    # # Keymap for 3D View Generic
    # km = kc.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
    # 
    # Keymap for Object-Non-modal
    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')

    # Add the Pie Menu keymap item
    keymap_item = km.keymap_items.new(
            idname='wm.call_menu_pie', # Operator to call a pie menu
            type='Q',
            value='PRESS',
            shift=True,
    )
    # Tell the operator which pie menu to call by its bl_idname
    keymap_item.properties.name = ui.pie_menu.VIEW3D_MT_RigBotEditPie.bl_idname

    # Store the keymap for removal on unregister
    addon_keymaps.append((km, keymap_item))

def unregister_keymaps():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if not kc:
        return # Nothing to remove if keyconfig is gone

    # Remove keymaps in reverse order or by iterating addon_keymaps
    for km, keymap_item in addon_keymaps:
        try:
            km.keymap_items.remove(keymap_item)
        except Exception as e:
            print(f"Warning: Could not remove keymap item: {e}")

    addon_keymaps.clear() # Clear the list
# --- End Keymap Handling ---

def register():
    operators.register()
    ui.register()
    register_keymaps()

def unregister():
    unregister_keymaps() # Unregister keymaps first
    operators.unregister()
    ui.unregister()

if __name__ == "__main__":
    register()