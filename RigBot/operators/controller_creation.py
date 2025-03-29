import bpy
from . import shape_library
class OBJECT_OT_place_controller(bpy.types.Operator):
    bl_idname = "object.place_controller"
    bl_label = "Place Controller"
    bl_description = "Places a controller shape at the location of the selected bone"

    def execute(self, context):
        obj = context.active_object
        scene = context.scene

        # Check if we are in Edit Mode of an Armature and a bone is active
        if not (obj and obj.type == 'ARMATURE' and context.mode == 'EDIT_ARMATURE' and obj.data.edit_bones.active):
            self.report({'WARNING'}, "Please select a bone in Edit Mode of an Armature.")
            return {'CANCELLED'}

        # Get the active edit bone
        selected_bone = obj.data.edit_bones.active # Use edit_bones in Edit Mode
        shape_type = scene.rigbot_controller_shape
        color = scene.rigbot_controller_color

        # --- Use Shape Library ---
        controller = None # Initialize controller variable

        if shape_type == 'CUBE':
            # Call the function from your shape library
            controller = shape_library.create_cube_controller(name=f"{selected_bone.name}_CTRL")
            # Ensure controller creation was successful
            if not controller:
                self.report({'ERROR'}, f"Failed to create CUBE shape from library.")
                return {'CANCELLED'}

        # --- Placeholder for future shapes ---
        elif shape_type == 'CIRCLE':
            # Placeholder - Using ops for now, replace with library call when implemented
            bpy.ops.curve.primitive_bezier_circle_add() # Use default location, position later
            controller = context.active_object
            if controller:
                controller.name = f"{selected_bone.name}_CTRL" # Name it consistently
            else:
                self.report({'ERROR'}, f"Failed to create CIRCLE shape.")
                return {'CANCELLED'}

        elif shape_type == 'SQUARE':
            # Placeholder - Using ops for now, replace with library call when implemented
            bpy.ops.mesh.primitive_plane_add() # Use default location, position later
            controller = context.active_object
            if controller:
                controller.name = f"{selected_bone.name}_CTRL" # Name it consistently
                # Optional rotation can be done during positioning/assignment
            else:
                self.report({'ERROR'}, f"Failed to create SQUARE shape.")
                return {'CANCELLED'}

        else: # This else should now only be reached if the shape_type is truly unrecognized
            self.report({'WARNING'}, f"Invalid controller shape selected: {shape_type}")
            return {'CANCELLED'}

        # --- Post-Creation Steps (Common to all shapes) ---

        # Link the created controller object to the scene
        context.collection.objects.link(controller)

        # Position the controller at the bone's head location (world space)
        # We need to transform the bone's head location from local armature space to world space
        armature_matrix = obj.matrix_world
        controller.location = armature_matrix @ selected_bone.head

        # Optional: Match controller orientation to bone (more complex)
        # This requires matrix math to align one of the controller's axes with the bone's Y axis
        # For simplicity, we'll just place it at the head for now.

        # Assign the controller as custom shape to the corresponding Pose Bone
        # Need to switch to Pose Mode briefly or access pose bones directly if possible
        pose_bone = obj.pose.bones.get(selected_bone.name)
        if pose_bone:
            pose_bone.custom_shape = controller
            # Optional: Scale the custom shape uniformly if needed
            # pose_bone.custom_shape_scale = 0.5
            # Optional: Hide the controller object itself from render/viewport
            controller.hide_set(True)
            controller.hide_render = True
        else:
            self.report({'WARNING'}, f"Could not find Pose Bone '{selected_bone.name}' to assign custom shape.")


        # Set the color (using Bone Color Groups is often preferred for rigging)
        # Applying material color might not be visible depending on viewport settings for wireframes.
        # A better approach for rigs is often using Bone Color Groups.
        # Example: Find or create a color set and assign it
        # This part might need further refinement based on desired coloring method.

        self.report({'INFO'}, f"Controller '{controller.name}' created and assigned to bone '{selected_bone.name}'.")
        # Make the armature the active object again, remain in Edit mode
        context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

# Ensure controller_creation.register() and unregister() are called in operators/__init__.py
# Ensure shape_library doesn't need registration itself (it only contains functions)

def register():
    bpy.utils.register_class(OBJECT_OT_place_controller)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_place_controller)