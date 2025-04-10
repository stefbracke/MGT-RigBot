import bpy

class RIGBOT_OT_armature_parent_keep_offset(bpy.types.Operator):
    """Parents selected bones to the active bone, keeping the offset (no pop-up)"""
    bl_idname = "rigbot.armature_parent_keep_offset"
    bl_label = "Parent Bone (Keep Offset)"
    bl_description = "Parent selected bones to active bone, keeping offset. Requires Edit Mode"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_ARMATURE' and
                context.active_object and
                context.active_object.type == 'ARMATURE' and
                context.active_bone is not None and
                len(context.selected_editable_bones) >= 2) # Need parent + at least one child

    def execute(self, context):
        try:
            bpy.ops.armature.parent_set(type='OFFSET')
            return {'FINISHED'}
        except RuntimeError as e:
            self.report({'ERROR'}, f"Failed to parent bones: {e}")
            return {'CANCELLED'}

def register():
    bpy.utils.register_class(RIGBOT_OT_armature_parent_keep_offset)

def unregister():
    bpy.utils.unregister_class(RIGBOT_OT_armature_parent_keep_offset)