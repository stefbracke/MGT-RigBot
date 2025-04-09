import bpy
from bpy.types import Menu # Type: ignore

# Pie Menu for Edit Mode Toggle and Snapping
class VIEW3D_MT_RigBotEditPie(Menu):
    bl_label = "RigBot Edit/Snap Pie"
    bl_idname = "VIEW3D_MT_rigbot_edit_pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        obj = context.active_object

        toggle_icon = 'OBJECT_DATAMODE' if obj and obj.mode == 'EDIT' else 'EDITMODE_HLT'
        pie.operator("object.editmode_toggle", text="Toggle Mode", icon=toggle_icon)
        pie.operator("view3d.snap_cursor_to_selected", text="Cursor to Selected", icon='CURSOR')
        pie.operator("view3d.snap_selected_to_cursor", text="Selected to Cursor", icon='RESTRICT_SELECT_OFF')
        pie.operator("object.posemode_toggle", text="Toggle Pose Mode", icon='POSE_HLT')

def register():
    bpy.utils.register_class(VIEW3D_MT_RigBotEditPie)

def unregister():
    bpy.utils.unregister_class(VIEW3D_MT_RigBotEditPie)