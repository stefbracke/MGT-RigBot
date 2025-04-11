import bpy


def poll_pose_mode(context):
    """Checks if context is valid for pose operators (Pose Mode, Armature, Selected Bones)."""
    return (context.active_object is not None and
            context.active_object.type == 'ARMATURE' and
            context.mode == 'POSE' and
            context.selected_pose_bones is not None) # Check for selected pose bones

class POSE_OT_reset_location(bpy.types.Operator):
    """Clears Location for all selected pose bones"""
    bl_idname = "pose.reset_location"
    bl_label = "Reset Pose Location"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_pose_mode(context)

    def execute(self, context):
        if not self.poll(context):
            self.report({'WARNING'}, "Operator cannot run in current context.")
            return {'CANCELLED'}
        try:
            bpy.ops.pose.loc_clear()
            self.report({'INFO'}, "Selected pose bone locations reset.")
        except RuntimeError as e:
            self.report({'ERROR'}, f"Failed to reset location: {e}")
            return {'CANCELLED'}
        return {'FINISHED'}

class POSE_OT_reset_rotation(bpy.types.Operator):
    """Clears Rotation for all selected pose bones"""
    bl_idname = "pose.reset_rotation"
    bl_label = "Reset Pose Rotation"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_pose_mode(context)

    def execute(self, context):
        if not self.poll(context):
            self.report({'WARNING'}, "Operator cannot run in current context.")
            return {'CANCELLED'}
        try:
            bpy.ops.pose.rot_clear()
            self.report({'INFO'}, "Selected pose bone rotations reset.")
        except RuntimeError as e:
            self.report({'ERROR'}, f"Failed to reset rotation: {e}")
            return {'CANCELLED'}
        return {'FINISHED'}

class POSE_OT_reset_scale(bpy.types.Operator):
    """Clears Scale for all selected pose bones"""
    bl_idname = "pose.reset_scale"
    bl_label = "Reset Pose Scale"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_pose_mode(context)

    def execute(self, context):
        if not self.poll(context):
            self.report({'WARNING'}, "Operator cannot run in current context.")
            return {'CANCELLED'}
        try:
            bpy.ops.pose.scale_clear()
            self.report({'INFO'}, "Selected pose bone scales reset.")
        except RuntimeError as e:
            self.report({'ERROR'}, f"Failed to reset scale: {e}")
            return {'CANCELLED'}
        return {'FINISHED'}

class POSE_OT_reset_transforms(bpy.types.Operator):
    """Clears Location, Rotation, and Scale for all selected pose bones"""
    bl_idname = "pose.reset_transforms"
    bl_label = "Reset All Pose Transforms"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_pose_mode(context)

    def execute(self, context):
        if not self.poll(context):
            self.report({'WARNING'}, "Operator cannot run in current context.")
            return {'CANCELLED'}
        try:
            # Call the individual clear operators for clarity and potential robustness
            bpy.ops.pose.loc_clear()
            bpy.ops.pose.rot_clear()
            bpy.ops.pose.scale_clear()
            self.report({'INFO'}, "Selected pose bone transforms reset.")
        except RuntimeError as e:
            self.report({'ERROR'}, f"Failed to reset transforms: {e}")
            return {'CANCELLED'}
        return {'FINISHED'}

# List of classes to register
classes = (
    POSE_OT_reset_location,
    POSE_OT_reset_rotation,
    POSE_OT_reset_scale,
    POSE_OT_reset_transforms,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)