import bpy

class OBJECT_OT_select_bone(bpy.types.Operator):
    bl_idname = "object.select_bone"
    bl_label = "Select Bone"
    bl_description = "Selects the bone in the 3D Viewport"

    bone_name: bpy.props.StringProperty(name="Bone Name", description="Name of the bone to select")

    def execute(self, context):
        obj = context.active_object
        if not (obj and obj.type == 'ARMATURE'):
            self.report({'WARNING'}, "No active armature found.")
            return {'CANCELLED'}

        armature = obj.data
        if self.bone_name not in armature.bones:
            self.report({'WARNING'}, f"Bone '{self.bone_name}' not found.")
            return {'CANCELLED'}

        current_mode = context.object.mode
        bpy.ops.object.mode_set(mode='EDIT')
        for bone in armature.edit_bones:
            bone.select = (bone.name == self.bone_name)
        bpy.ops.object.mode_set(mode=current_mode)

        return {'FINISHED'}

class OBJECT_OT_rename_bone(bpy.types.Operator):
    bl_idname = "object.rename_bone"
    bl_label = "Rename Bone"
    bl_description = "Rename the selected bone"

    bone_name: bpy.props.StringProperty(name="Current Bone Name", description="Name of the bone to rename")
    new_name: bpy.props.StringProperty(name="New Bone Name", description="New name for the bone")

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        obj = context.active_object
        if not (obj and obj.type == 'ARMATURE'):
            self.report({'WARNING'}, "No active armature found.")
            return {'CANCELLED'}

        armature = obj.data
        if obj.mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')

        if self.bone_name not in armature.edit_bones:
            self.report({'WARNING'}, f"Bone '{self.bone_name}' not found in Edit Mode.")
            return {'CANCELLED'}

        armature.edit_bones[self.bone_name].name = self.new_name
        self.report({'INFO'}, f"Bone renamed to '{self.new_name}'.")

        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_OT_select_bone)
    bpy.utils.register_class(OBJECT_OT_rename_bone)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_rename_bone)
    bpy.utils.unregister_class(OBJECT_OT_select_bone)