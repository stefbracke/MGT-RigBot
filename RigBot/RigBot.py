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
        layout.operator("mesh.primitive_cube_add", text="Test Cube", icon="MESH_CUBE")
        layout.operator(
            "mesh.primitive_cylinder_add", text="Test Cylinder", icon="MESH_CYLINDER"
        )
        layout.operator(
            "mesh.primitive_uv_sphere_add", text="Test Cylinder", icon="SPHERE"
        )


def register():
    bpy.utils.register_class(SimpleUIPanel)


def unregister():
    bpy.utils.unregister_class(SimpleUIPanel)


if __name__ == "__main__":
    register()
