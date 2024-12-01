import bpy
import mathutils


class OBJECT_OT_add_bone(bpy.types.Operator):
    """Add a bone at the center of the selected object"""

    bl_idname = "object.add_bone_at_median"
    bl_label = "Add Bone at Median of Vertices"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        selected_objects = context.selected_objects  # type: ignore

        if not selected_objects:
            self.report({"WARNING"}, "No objects selected")
            return {"CANCELLED"}

        for obj in selected_objects:
            if obj.type != "MESH":
                self.report({"INFO"}, f"Skipped non-mesh object: {obj.name}")
                continue
            # Calculate the median point of all vertices
            mesh = obj.data
            median = mathutils.Vector((0, 0, 0))
            for vertex in mesh.vertices:  # type: ignore
                median += obj.matrix_world @ vertex.co  # Transform to world space
            median /= len(mesh.vertices)  # type: ignore

            # Create a new armature
            bpy.ops.object.armature_add(enter_editmode=False, location=median)

        return {"FINISHED"}


class VIEW3D_PT_SimpleUIPanel(bpy.types.Panel):
    bl_label = "Mechanical Rig Pro"
    bl_idname = "VIEW3D_PT_simple_ui_frame"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Add Bone Tools")
        layout.operator(OBJECT_OT_add_bone.bl_idname, text="Add Bone at Median")


def register():
    bpy.utils.register_class(OBJECT_OT_add_bone)
    bpy.utils.register_class(VIEW3D_PT_SimpleUIPanel)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_bone)
    bpy.utils.unregister_class(VIEW3D_PT_SimpleUIPanel)


if __name__ == "__main__":
    register()
