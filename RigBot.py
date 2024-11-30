import bpy


class SimpleUIPanel(bpy.types.Panel):
    bl_label = "Mechanical Rig Pro"
    bl_idname = "VIEW3D_PT_simple_ui_frame"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Test description!")
        layout.operator("mesh.primitive_cube_add", text="Test Button")


def register():
    bpy.utils.register_class(SimpleUIPanel)


def unregister():
    bpy.uti


if __name__ == "__main__":
    register()
