import bpy
from . import shape_library

# +++ Helper function +++
def find_or_create_bone_group(armature_object, color_set_id: str):
    """Finds an existing BoneGroup with the color_set_id, or creates one."""
    if not armature_object or armature_object.type != 'ARMATURE':
        return None

    bone_groups = armature_object.pose.bone_groups

    # Check if a group with this color set already exists
    for group in bone_groups:
        if group.color_set == color_set_id:
            return group

    # If not found, create a new one
    try:
        base_name = f"ColorSet_{color_set_id.split('_')[-1]}"
        group_name = base_name
        count = 1
        while group_name in bone_groups:
            group_name = f"{base_name}_{count}"
            count += 1

        new_group = bone_groups.new(name=group_name)
        new_group.color_set = color_set_id
        print(f"Created new Bone Group: '{new_group.name}' for Color Set '{color_set_id}'")
        return new_group
    except Exception as e:
        print(f"Error creating new bone group for {color_set_id}: {e}")
        return None
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    
class OBJECT_OT_place_controller(bpy.types.Operator):
    bl_idname = "object.place_controller"
    bl_label = "Place Controller"
    bl_description = "Places a controller shape at the location of the selected bone"

    def execute(self, context):
        obj = context.active_object
        scene = context.scene
        
        current_mode = context.mode
        if current_mode != 'POSE':
            try:
                bpy.ops.object.mode_set(mode='POSE')
            except Exception as e:
                # Handle cases where switching mode isn't possible (e.g. no armature selected)
                self.report({'WARNING'}, f"Could not switch to Pose Mode: {e}. Active bone needed.")
                return {'CANCELLED'}

        # Get the active pose bone
        selected_bone = context.active_pose_bone
        if not (obj and obj.type == 'ARMATURE' and selected_bone):
            self.report({'WARNING'}, "Please select a bone in Pose Mode of an Armature.")
            # Switch back to original mode if we changed it
            if current_mode != 'POSE':
                bpy.ops.object.mode_set(mode=current_mode)
            return {'CANCELLED'}

        shape_type = scene.rigbot_controller_shape
        color_set_id = scene.rigbot_bone_color_choice
        # -----------------------

        # --- Use Shape Library ---
        controller = None
        shape_name = f"WGT_{selected_bone.name}"

        if shape_type == 'CUBE':
            controller = shape_library.create_cube_shape(name=f"{selected_bone.name}_CTRL")
            if not controller:
                self.report({'ERROR'}, f"Failed to create CUBE shape from library.")
                return {'CANCELLED'}

        elif shape_type == 'CIRCLE':
            controller = shape_library.create_circle_shape(name=f"{selected_bone.name}_CTRL")
            if not controller:
                self.report({'ERROR'}, f"Failed to create CIRCLE shape.")
                return {'CANCELLED'}

        elif shape_type == 'PLANE':
            controller = shape_library.create_plane_shape(name=f"{selected_bone.name}_CTRL")
            if not controller:
                self.report({'ERROR'}, f"Failed to create PLANE shape.")
                return {'CANCELLED'}

        else:
            self.report({'WARNING'}, f"Invalid controller shape selected: {shape_type}")
            return {'CANCELLED'}

        # --- Post-Creation Steps (Common to all shapes) ---

        # Link the created controller object to the scene
        if controller.name not in context.collection.objects:
            context.collection.objects.link(controller)

        # Position the controller at the bone's head location (world space)
        # We need to transform the bone's head location from local armature space to world space
        armature_matrix = obj.matrix_world
        controller.location = armature_matrix @ selected_bone.head
        controller.rotation_euler = (0, 0, 0)  # Reset rotation to avoid any unwanted transformations

        # Optional: Match controller orientation to bone (more complex)
        # This requires matrix math to align one of the controller's axes with the bone's Y axis
        # For simplicity, we'll just place it at the head for now.
        
        target_group = find_or_create_bone_group(obj, color_set_id)
        if target_group:
            selected_bone.bone_group = target_group
            self.report({'INFO'}, f"Controller '{controller.name}' created, assigned to bone '{selected_bone.name}', and set to color group '{target_group.name}'.")
        else:
            self.report({'WARNING'}, f"Controller '{controller.name}' created and assigned, but failed to set bone color group.")
        # Switch back to original mode if we changed it
        if current_mode != obj.mode:
            bpy.ops.object.mode_set(mode=current_mode)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_OT_place_controller)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_place_controller)