import bpy


class OBJECT_OT_add_bone(bpy.types.Operator):
    """Add a bone at the center of the selected object"""

    bl_idname = "object.add_bone_at_center"
    bl_label = "Add Bone at Object Center"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        if not context:
            self.report({"WARNING"}, "No context")
            return {"CANCELLED"}
        obj = context.active_object

        if not obj:
            self.report({"WARNING"}, "No active object")
            return {"CANCELLED"}
        # Get the location of the object's origin
        obj_center = (
            obj.location
        )  # might have to do this according to vertex position average instead

        # Create a new armature
        bpy.ops.object.armature_add(enter_editmode=False, location=obj_center)

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
        layout.operator(OBJECT_OT_add_bone.bl_idname, text="Add Bone at Center")


def register():
    bpy.utils.register_class(OBJECT_OT_add_bone)
    bpy.utils.register_class(VIEW3D_PT_SimpleUIPanel)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_bone)
    bpy.utils.unregister_class(VIEW3D_PT_SimpleUIPanel)


if __name__ == "__main__":
    register()
