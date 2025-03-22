import bpy

class VIEW3D_PT_RigBotPanel(bpy.types.Panel):
    bl_label = "RigBot"
    bl_idname = "VIEW3D_PT_RigBotPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RigBot"

    def draw(self, context):
        layout = self.layout

def register():
    bpy.utils.register_class(VIEW3D_PT_RigBotPanel)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_RigBotPanel)
