import bpy

class RIGBOT_OT_pose_add_damped_track_self(bpy.types.Operator):
    """Adds a Damped Track constraint to the active pose bone, targeting the armature itself"""
    bl_idname = "rigbot.pose_add_damped_track_self"
    bl_label = "Add Damped Track (Target Self)"
    bl_description = "Add a Damped Track constraint to the active pose bone, targeting the Armature object"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # Requires Pose Mode, an active object that is an armature, and an active pose bone
        return (context.mode == 'POSE' and
                context.object and
                context.object.type == 'ARMATURE' and
                context.active_pose_bone is not None)

    def execute(self, context):
        armature_obj = context.object
        active_pose_bone = context.active_pose_bone

        if not active_pose_bone:
            # Poll should prevent this, but good practice to check
            self.report({'WARNING'}, "No active pose bone selected.")
            return {'CANCELLED'}

        # Add the constraint
        try:
            # Store constraint count before adding
            constraint_count = len(active_pose_bone.constraints)
            bpy.ops.pose.constraint_add(type='DAMPED_TRACK')

            # Check if a new constraint was actually added
            if len(active_pose_bone.constraints) > constraint_count:
                new_constraint = active_pose_bone.constraints[-1] # Get the last added constraint

                # Verify it's the correct type (should be, but check)
                if new_constraint.type == 'DAMPED_TRACK':
                    # Set the target to the armature object itself
                    new_constraint.target = armature_obj
                    self.report({'INFO'}, f"Added Damped Track to '{active_pose_bone.name}', target set to '{armature_obj.name}'.")
                    return {'FINISHED'}
                else:
                    # This shouldn't happen if operator call worked
                    self.report({'WARNING'}, f"Added constraint was not Damped Track (Type: {new_constraint.type}). Target not set.")
                    # Optionally remove the wrongly added constraint:
                    # active_pose_bone.constraints.remove(new_constraint)
                    return {'CANCELLED'}
            else:
                self.report({'WARNING'}, "Damped Track constraint could not be added.")
                return {'CANCELLED'}

        except RuntimeError as e:
            self.report({'ERROR'}, f"Failed to add Damped Track constraint: {e}")
            return {'CANCELLED'}

class RIGBOT_OT_pose_add_stretch_to(bpy.types.Operator):
    """Adds a Stretch To constraint to the active pose bone"""
    bl_idname = "rigbot.pose_add_stretch_to"
    bl_label = "Add Stretch To"
    bl_description = "Add a Stretch To constraint to the active pose bone"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # Requires Pose Mode, an active object that is an armature, and an active pose bone
        return (context.mode == 'POSE' and
                context.object and
                context.object.type == 'ARMATURE' and
                context.active_pose_bone is not None)

    def execute(self, context):
        armature_obj = context.object
        active_pose_bone = context.active_pose_bone

        if not active_pose_bone:
            self.report({'WARNING'}, "No active pose bone selected.")
            return {'CANCELLED'}

        # Add the constraint
        try:
            # Store constraint count before adding
            constraint_count = len(active_pose_bone.constraints)
            bpy.ops.pose.constraint_add(type='STRETCH_TO')

            # Check if a new constraint was actually added
            if len(active_pose_bone.constraints) > constraint_count:
                new_constraint = active_pose_bone.constraints[-1] # Get the last added constraint

                # Verify it's the correct type
                if new_constraint.type == 'STRETCH_TO':
                    new_constraint.target = armature_obj
                    self.report({'INFO'}, f"Added Stretch To constraint to '{active_pose_bone.name}'.")
                    return {'FINISHED'}
                else:
                    self.report({'WARNING'}, f"Added constraint was not Stretch To (Type: {new_constraint.type}).")
                    return {'CANCELLED'}
            else:
                self.report({'WARNING'}, "Stretch To constraint could not be added.")
                return {'CANCELLED'}

        except RuntimeError as e:
            self.report({'ERROR'}, f"Failed to add Stretch To constraint: {e}")
            return {'CANCELLED'}

class RIGBOT_OT_pose_add_ik(bpy.types.Operator):
    """Adds an Inverse Kinematics (IK) constraint to the active pose bone"""
    bl_idname = "rigbot.pose_add_ik"
    bl_label = "Add IK Constraint"
    bl_description = "Add an Inverse Kinematics (IK) constraint to the active pose bone"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # Requires Pose Mode, an active object that is an armature, and an active pose bone
        return (context.mode == 'POSE' and
                context.object and
                context.object.type == 'ARMATURE' and
                context.active_pose_bone is not None)

    def execute(self, context):
        active_pose_bone = context.active_pose_bone

        if not active_pose_bone:
            self.report({'WARNING'}, "No active pose bone selected.")
            return {'CANCELLED'}

        # Add the constraint
        try:
            constraint_count = len(active_pose_bone.constraints)
            bpy.ops.pose.constraint_add(type='IK')

            # Check if a new constraint was actually added
            if len(active_pose_bone.constraints) > constraint_count:
                new_constraint = active_pose_bone.constraints[-1] # Get the last added constraint

                # Verify it's the correct type
                if new_constraint.type == 'IK':
                    # --- Set some common default values ---
                    new_constraint.chain_count = 0 # Default to full chain length
                    new_constraint.use_tail = True  # Often desired for IK
                    # Targets (target, pole_target) usually need manual assignment
                    # --- End Defaults ---

                    self.report({'INFO'}, f"Added IK constraint to '{active_pose_bone.name}'.")
                    return {'FINISHED'}
                else:
                    self.report({'WARNING'}, f"Added constraint was not IK (Type: {new_constraint.type}).")
                    # Optionally remove the wrongly added constraint:
                    # active_pose_bone.constraints.remove(new_constraint)
                    return {'CANCELLED'}
            else:
                self.report({'WARNING'}, "IK constraint could not be added.")
                return {'CANCELLED'}

        except RuntimeError as e:
            self.report({'ERROR'}, f"Failed to add IK constraint: {e}")
            return {'CANCELLED'}
        
classes = (
    RIGBOT_OT_pose_add_damped_track_self,
    RIGBOT_OT_pose_add_stretch_to,
    RIGBOT_OT_pose_add_ik,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
