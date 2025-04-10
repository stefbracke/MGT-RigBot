import bpy

class OBJECT_OT_parent_by_name(bpy.types.Operator):
    """Parents selected objects to bones of the active armature if names match"""
    bl_idname = "object.parent_by_name"
    bl_label = "Parent Objects to Bones by Name"
    bl_description = "Parents selected objects to bones in the active armature where object name matches bone name"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # Requires an active object that is an armature, and at least one other selected object
        active_obj = context.active_object
        return (active_obj is not None and
                active_obj.type == 'ARMATURE' and
                len(context.selected_objects) > 1) # Need armature + at least one child

    def execute(self, context):
        armature_obj = context.active_object
        if not (armature_obj and armature_obj.type == 'ARMATURE'):
            # Poll should prevent this, but double-check
            self.report({'WARNING'}, "Active object must be an Armature.")
            return {'CANCELLED'}

        # Store original context
        original_mode = armature_obj.mode
        original_active = context.view_layer.objects.active
        original_selection = context.selected_objects[:] # Make a copy

        # Get potential children (all selected objects EXCEPT the armature)
        selected_children = [obj for obj in context.selected_objects if obj != armature_obj]

        if not selected_children:
            self.report({'INFO'}, "No other objects selected besides the armature to parent.")
            return {'CANCELLED'}

        armature_data = armature_obj.data
        parented_count = 0
        failed_parents = []

        # Create a dictionary of bones for faster lookup
        bones_dict = {bone.name: bone for bone in armature_data.bones}

        # Ensure Object Mode for parenting operations
        if original_mode != 'OBJECT':
            try:
                bpy.ops.object.mode_set(mode='OBJECT')
            except RuntimeError as e:
                self.report({'ERROR'}, f"Could not switch to Object Mode: {e}")
                return {'CANCELLED'}

        # --- Iterate and Parent ---
        for child_obj in selected_children:
            if child_obj.name in bones_dict:
                bone_name = child_obj.name
                target_bone = bones_dict[bone_name]
                print(f"Match found: Object '{child_obj.name}' and Bone '{bone_name}'") # Debug info

                # --- Parenting Process ---
                try:
                    # 1. Deselect all first for clean state
                    bpy.ops.object.select_all(action='DESELECT')

                    # 2. Select child and armature, make armature active
                    child_obj.select_set(True)
                    armature_obj.select_set(True)
                    context.view_layer.objects.active = armature_obj # Essential for parenting context

                    # 3. Set the target bone as the armature's active bone
                    #    Needs to be done *before* potentially switching mode
                    armature_data.bones.active = target_bone

                    # 4. Switch to Pose Mode - Required for 'BONE' type parenting
                    bpy.ops.object.mode_set(mode='POSE')

                    # 5. Parent to the active bone (set in step 3)
                    #    Check if already parented to avoid errors (optional but good)
                    if child_obj.parent != armature_obj or child_obj.parent_bone != bone_name:
                        bpy.ops.object.parent_set(type='BONE')
                        parented_count += 1
                        print(f"Successfully parented '{child_obj.name}' to bone '{bone_name}'") # Debug
                    else:
                        print(f"'{child_obj.name}' already parented correctly to bone '{bone_name}'. Skipping.") # Debug


                    # 6. Switch back to Object mode for the next object
                    bpy.ops.object.mode_set(mode='OBJECT')

                except Exception as e:
                    failed_parents.append(child_obj.name)
                    self.report({'WARNING'}, f"Failed parenting '{child_obj.name}' to bone '{bone_name}': {e}")
                    # Attempt to return to object mode if error occurred mid-process
                    if context.object and context.object.mode != 'OBJECT':
                        try:
                            bpy.ops.object.mode_set(mode='OBJECT')
                        except RuntimeError: pass # Ignore if fails


        # --- Cleanup ---
        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')
        # Restore original selection
        for obj in original_selection:
            try:
                obj.select_set(True)
            except ReferenceError:
                pass # Object might have been deleted or is invalid
        # Restore original active object
        try:
            context.view_layer.objects.active = original_active
        except ReferenceError:
            pass # Original active might be invalid
        # Restore original mode if it changed and possible
        if context.object and context.object.mode != original_mode:
            try:
                bpy.ops.object.mode_set(mode=original_mode)
            except RuntimeError: pass # Ignore if fails


        # Final report
        report_message = f"Parented {parented_count} object(s) by name."
        if failed_parents:
            report_message += f" Failed to parent: {', '.join(failed_parents)}."
        self.report({'INFO'}, report_message)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_OT_parent_by_name)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_parent_by_name)