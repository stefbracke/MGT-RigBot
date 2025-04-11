import bpy

class OBJECT_OT_add_initial_bone(bpy.types.Operator):
    bl_idname = "object.add_initial_bone"
    bl_label = "Add Initial Bone"
    bl_description = "Creates an initial bone and switches to Edit Mode"

    def execute(self, context):
        if context.active_object and context.active_object.type == 'ARMATURE':
            self.report({'WARNING'}, "An armature is already active. Deselect it to add a new initial bone.")
            return {'CANCELLED'}

        bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
        obj = context.active_object
        if obj and obj.type == 'ARMATURE':
            obj.data.show_axes = True
            obj.data.show_names = True
            obj.show_in_front = True

        self.report({'INFO'}, "Initial bone added with viewport display options enabled.")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_OT_add_initial_bone)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_initial_bone)
