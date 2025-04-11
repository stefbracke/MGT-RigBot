import bpy

class OBJECT_OT_select_bone(bpy.types.Operator):
    bl_idname = "object.select_bone"
    bl_label = "Select Bone"
    bl_description = "Selects the bone in the 3D Viewport"

    bone_name: bpy.props.StringProperty(name="Bone Name", description="Name of the bone to select")

    def execute(self, context):
        obj = context.active_object
        scene = context.scene
        if not (obj and obj.type == 'ARMATURE'):
            self.report({'WARNING'}, "No active armature found.")
            return {'CANCELLED'}

        armature = obj.data
        if self.bone_name not in armature.bones:
            self.report({'WARNING'}, f"Bone '{self.bone_name}' not found in armature '{armature.name}'.")
            scene.rigbot_bone_index = -1 # Reset index if bone not found
            return {'CANCELLED'}
        
        target_bone = armature.bones[self.bone_name]
        target_index = -1
        try:
            # Find the index of the bone in the collection
            target_index = armature.bones.find(self.bone_name)
        except ValueError:
            self.report({'WARNING'}, f"Could not find index for bone '{self.bone_name}'.")
            scene.rigbot_bone_index = -1 # Reset index if finding fails
            return {'CANCELLED'}

        current_mode = obj.mode
        
        # 1. Deselect all bones in the current mode
        try:
            if current_mode == 'EDIT':
                # Ensure we are in edit mode before calling edit mode operator
                if obj.mode != 'EDIT': bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.armature.select_all(action='DESELECT')
            elif current_mode == 'POSE':
                if obj.mode != 'POSE': bpy.ops.object.mode_set(mode='POSE')
                bpy.ops.pose.select_all(action='DESELECT')
            else: # Object mode - deselect base bones
                for bone in armature.bones:
                    bone.select = False
        except RuntimeError as e:
            print(f"Note: Could not deselect all bones ({e})")
            
        # 2. Select the target bone
        target_bone.select = True
        
        # 3. Set the active bone
        armature.bones.active = target_bone
        
        # 4. Ensure visual selection in Pose Mode
        if current_mode == 'EDIT':
            # Ensure we are back in edit mode if we switched
            if obj.mode != 'EDIT': bpy.ops.object.mode_set(mode='EDIT')
            edit_bone = armature.edit_bones.get(self.bone_name)
            if edit_bone:
                armature.edit_bones.active = edit_bone # Set active EditBone
                edit_bone.select = True # Ensure selection in edit mode

        elif current_mode == 'POSE':
            if obj.mode != 'POSE': bpy.ops.object.mode_set(mode='POSE')
            pose_bone = obj.pose.bones.get(self.bone_name)
            if pose_bone:

                pose_bone.bone.select = True 
                pass

        # 5. Update the scene property for UI list highlighting *AFTER* selection
        if target_index != -1:
            scene.rigbot_bone_index = target_index
        else:
            scene.rigbot_bone_index = -1 # Safety reset
        return {'FINISHED'}

class OBJECT_OT_rename_bone(bpy.types.Operator):
    """ Renames the selected bone """
    bl_idname = "object.rename_bone"
    bl_label = "Rename Bone"
    bl_description = "Rename the selected bone"
    bl_options = {'REGISTER', 'UNDO'}

    new_name: bpy.props.StringProperty(
            name="New Bone Name", 
            description="New name for the bone")

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        if not (obj and obj.type == 'ARMATURE'):
            return False

        if obj.mode == 'EDIT':
            # Check for active EditBone
            return obj.data.edit_bones.active is not None
        elif obj.mode == 'POSE':
            # Check active_pose_bone wrapper (which exists if armature.bones.active is set)
            return context.active_pose_bone is not None
        else: # Object mode
            # Check for active ArmatureBone
            return obj.data.bones.active is not None
        
    def invoke(self, context, event):
        obj = context.active_object
        active_bone_to_rename = None
    
        if obj.mode == 'EDIT':
            active_bone_to_rename = obj.data.edit_bones.active
        elif obj.mode == 'POSE':
            active_pose_bone = context.active_pose_bone
            if active_pose_bone:
                active_bone_to_rename = active_pose_bone.bone
        else: # Object mode
            active_bone_to_rename = obj.data.bones.active
    
        if not active_bone_to_rename:
            self.report({'WARNING'}, "No active bone found to rename.")
            return {'CANCELLED'}
    
        self.new_name = active_bone_to_rename.name
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        obj = context.active_object
        active_bone_to_rename = None

        # Re-determine the active bone based on the mode for execution safety
        if obj.mode == 'EDIT':
            active_bone_to_rename = obj.data.edit_bones.active
        elif obj.mode == 'POSE':
            active_pose_bone = context.active_pose_bone
            if active_pose_bone:
                active_bone_to_rename = active_pose_bone.bone # Target the underlying ArmatureBone
        else: # Object mode
            active_bone_to_rename = obj.data.bones.active

        if not active_bone_to_rename:
            self.report({'ERROR'}, "No active bone found. Cannot rename.")
            return {'CANCELLED'}

        if not self.new_name or self.new_name == active_bone_to_rename.name:
            return {'CANCELLED'}
        if self.new_name in obj.data.bones and self.new_name != active_bone_to_rename.name:
            self.report({'WARNING'}, f"Bone name '{self.new_name}' already exists.")
            return {'CANCELLED'}

        try:
            original_name = active_bone_to_rename.name
            active_bone_to_rename.name = self.new_name
            self.report({'INFO'}, f"Bone '{original_name}' renamed to '{self.new_name}'.")
            context.scene.rigbot_bone_index = obj.data.bones.find(self.new_name) # Update index to renamed bone

        except Exception as e: # Catch potential errors
            self.report({'ERROR'}, f"Failed to rename bone: {e}")
            return {'CANCELLED'}

        return {'FINISHED'}

classes = (
    OBJECT_OT_select_bone,
    OBJECT_OT_rename_bone,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)