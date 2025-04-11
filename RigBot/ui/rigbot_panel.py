import bpy

class VIEW3D_PT_RigBotPanel(bpy.types.Panel):
    bl_label = "RigBot"
    bl_idname = "VIEW3D_PT_RigBotPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RigBot"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.active_object
            
        # --- Skeleton Creation Panel ---
        # Main header row for Skeleton Creation panel
        header_row_skeleton = layout.row(align=True)
        arrow_icon_skeleton = 'TRIA_DOWN' if scene.rigbot_panel_expanded else 'TRIA_RIGHT'
        header_row_skeleton.prop(scene, "rigbot_panel_expanded", text="", icon=arrow_icon_skeleton, emboss=False)
        header_row_skeleton.label(text="Skeleton", icon='ARMATURE_DATA')

        # Draw Skeleton Creation content only if expanded
        if scene.rigbot_panel_expanded:
            # Section: Bone Creation (Visible if no Armature is active)
            if not (obj and obj.type == 'ARMATURE'):
                box = layout.box()
                box.label(text="Bone Creation", icon='OUTLINER_OB_ARMATURE')
                col = box.column(align=True)
                col.operator("object.add_initial_bone", text="Add Initial Bone", icon='BONE_DATA')

            # Section: Bone List (Outliner View using UIList) - Shown when armature is active
            if context.active_object and context.active_object.type == 'ARMATURE':
                layout.separator()
                box_list = layout.box()
                box_list.label(text="Bone List", icon='BONE_DATA')
                box_list.template_list("BONE_UL_list", "", context.active_object.data, "bones", scene, "rigbot_bone_index", rows=5)
                # Rename button for the active bone
                box_list.operator("object.rename_bone", text="Rename Active Bone")

        layout.separator()

        # --- Skinning Panel ---
        header_row_skinning = layout.row(align=True)
        arrow_icon_skinning = 'TRIA_DOWN' if scene.rigbot_skinning_panel_expanded else 'TRIA_RIGHT'
        header_row_skinning.prop(scene, "rigbot_skinning_panel_expanded", text="", icon=arrow_icon_skinning, emboss=False)
        header_row_skinning.label(text="Skinning", icon='MOD_MESHDEFORM')

        if scene.rigbot_skinning_panel_expanded:
            box = layout.box()
            col = box.column(align=True)
            
            col.label(text="Object Parenting:")
            col.operator("rigbot.armature_parent_keep_offset", text="Parent Bone to Bone (Keep Offset)", icon='LINKED')
            
            # --- Parent by Name ---
            col.operator("object.parent_by_name", text="Parent by Name", icon='AUTOMERGE_ON')
            col.separator() 

            # Parent to Bone button
            parent_op = col.operator(
                    "object.parent_set",
                    text="Skin Mesh to Bone",
                    icon='CONSTRAINT_BONE' # Or 'CONSTRAINT_BONE' or 'LINKED'
            )
            parent_op.type = 'BONE' # Set the parenting type
            
            # Clear Parent button
            clear_parent_op = col.operator(
                    "object.parent_clear",
                    text="Clear Parent (Keep Transform)",
                    icon='X'
            )
            clear_parent_op.type = 'CLEAR_KEEP_TRANSFORM'

        layout.separator()
        
        # --- Constraints Panel ---
        header_row_constraints = layout.row(align=True)
        arrow_icon_constraints = 'TRIA_DOWN' if scene.rigbot_constraints_panel_expanded else 'TRIA_RIGHT'
        header_row_constraints.prop(scene, "rigbot_constraints_panel_expanded", text="", icon=arrow_icon_constraints, emboss=False)
        header_row_constraints.label(text="Constraints", icon='CONSTRAINT_BONE')

        if scene.rigbot_constraints_panel_expanded:
            box = layout.box()
            col = box.column(align=True)
            # Add Damped Track Constraint
            col.operator(
                    "rigbot.pose_add_damped_track_self",
                    text="Add Damped Track (Target Self)",
                    icon='CON_TRACKTO'
            )
            # Add Stretch To Constraint
            col.operator(
                    "rigbot.pose_add_stretch_to",
                    text="Add Stretch To",
                    icon='CON_STRETCHTO'
            )
            # Add Inverse Kinematics
            col.operator(
                    "rigbot.pose_add_ik",
                    text="Add Inverse Kinematics",
                    icon='CON_KINEMATIC'
            )
            
            # --- Display Existing Constraints ---
            pbone = context.active_pose_bone # Get the active pose bone

            # Check if in pose mode and a pose bone is active
            if context.mode == 'POSE' and pbone:
                if not pbone.constraints:
                    box.label(text="Active bone has no constraints.", icon='INFO')
                else:
                    # Iterate through constraints of the active pose bone
                    for constraint in pbone.constraints:
                        # Create a sub-box for each constraint for better organization
                        constraint_box = box.box()
                        # Allow expanding/collapsing constraint details
                        constraint_box.prop(constraint, "show_expanded", text=constraint.name, icon='CON_TRACKTO')

                        if constraint.show_expanded:
                            # Use layout.prop() with the constraint object and its property name (data path)
                            # The data paths you provided are attributes of the constraint object itself.

                            # Common Constraint Properties
                            constraint_box.prop(constraint, "name", text="Name") # pose.bones[...].constraints[...].name
                            constraint_box.prop(constraint, "target", text="Target") # pose.bones[...].constraints[...].target
                            # Subtarget Property (Requires prop_search)
                            # Check if the constraint type *has* a subtarget (like Damped Track, IK, etc.)
                            if hasattr(constraint, "subtarget"):
                                if constraint.target:
                                    constraint_box.prop_search(
                                            constraint,              # The constraint object
                                            "subtarget",             # The property name (data path)
                                            constraint.target.data,  # Search within the target armature's data
                                            "bones",                 # Search within the 'bones' collection
                                            text="Bone"              # Label for the UI element
                                    ) # pose.bones[...].constraints[...].subtarget
                            constraint_box.prop(constraint, "head_tail", text="Head/Tail") # pose.bones[...].constraints[...].head_tail
                            # Constraint-Specific Properties (Example: Damped Track)
                            if constraint.type == 'DAMPED_TRACK':
                                constraint_box.prop(constraint, "track_axis") # pose.bones[...].constraints[...].track_axis
                                constraint_box.prop(constraint, "influence", slider=True)
                            elif constraint.type == 'STRETCH_TO':
                                constraint_box.prop(constraint, "rest_length")
                                constraint_box.prop(constraint, "bulge")
                                constraint_box.prop(constraint, "volume")
                                constraint_box.prop(constraint, "keep_axis")
                                constraint_box.prop(constraint, "influence", slider=True)
                            # --- ADD THIS ELIF BLOCK for IK ---
                            elif constraint.type == 'IK':
                                # constraint_box.prop(constraint, "pole_target", text="Pole Target")
                                # if constraint.pole_target and constraint.pole_target.type == 'ARMATURE':
                                #     constraint_box.prop_search(
                                #             constraint,              # The constraint object
                                #             "pole_subtarget",        # The property name for pole bone
                                #             constraint.pole_target.data, # Search within the pole target armature's data
                                #             "bones",                 # Search within the 'bones' collection
                                #             text="Pole Bone"         # Label for the UI element
                                #     )
                                # constraint_box.prop(constraint, "pole_angle", text="Pole Angle") # Often useful with pole target
                                # constraint_box.separator()
                                # constraint_box.prop(constraint, "iterations")
                                constraint_box.prop(constraint, "chain_count", text="Chain Length") # Use chain_count for length
                                # constraint_box.prop(constraint, "use_tail")
                                # constraint_box.prop(constraint, "use_stretch")
                                # constraint_box.separator()
                                # constraint_box.label(text="Weighting:") # Header for weights
                                # constraint_box.prop(constraint, "weight", text="Position") # weight controls position
                                # constraint_box.prop(constraint, "orient_weight", text="Rotation") # orient_weight controls rotation
                                # constraint_box.separator()
                                constraint_box.prop(constraint, "influence", slider=True)
                            # --- END OF ADDED IK BLOCK ---
            elif context.mode != 'POSE':
                box.label(text="Switch to Pose Mode to see constraints.", icon='INFO')
            elif not pbone:
                box.label(text="Select a Bone to see its constraints.", icon='INFO')


        layout.separator()
            
        # --- Posing Panel ---
        header_row_posing = layout.row(align=True)
        arrow_icon_posing = 'TRIA_DOWN' if scene.rigbot_posing_panel_expanded else 'TRIA_RIGHT'
        header_row_posing.prop(scene, "rigbot_posing_panel_expanded", text="", icon=arrow_icon_posing, emboss=False)
        header_row_posing.label(text="Posing", icon='POSE_HLT')
        
        if scene.rigbot_posing_panel_expanded:
            box = layout.box()
            col = box.column(align=True) # Use a column for layout

            col.operator("pose.reset_location", text="Reset Location", icon='CON_LOCLIKE') # Use a suitable icon
            col.operator("pose.reset_rotation", text="Reset Rotation", icon='CON_ROTLIKE') # Use a suitable icon
            col.operator("pose.reset_scale", text="Reset Scale", icon='CON_SIZELIKE') # Use a suitable icon

            col.separator() # Add a separator for visual clarity

            col.operator("pose.reset_transforms", text="Reset Transforms", icon='FILE_REFRESH')


class BONE_UL_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            select_op = row.operator("object.select_bone", text=item.name, emboss=False)
            select_op.bone_name = item.name
            
            if item.parent:
                row.label(text=f"(Parent: {item.parent.name})", icon='BLANK1')
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon='BONE_DATA')

def register():
    bpy.types.Scene.rigbot_panel_expanded = bpy.props.BoolProperty(
            name="Expand RigBot Panel", default=True,
            description="Toggle display of the RigBot panel"
    )
    bpy.types.Scene.rigbot_bone_index = bpy.props.IntProperty(
            name="Bone Index", default=-1,
            description="Active bone index in the RigBot Bone List"
    )
    bpy.types.Scene.rigbot_constraints_panel_expanded = bpy.props.BoolProperty(
            name="Expand Constraints Panel", default=True,
            description="Toggle display of the Constraints panel"
    )
    bpy.types.Scene.rigbot_skinning_panel_expanded = bpy.props.BoolProperty(
            name="Expand Skinning Panel", default=True,
            description="Toggle display of the Skinning panel"
    )
    bpy.types.Scene.rigbot_posing_panel_expanded = bpy.props.BoolProperty(
            name="Expand Posing Panel", default=True,
            description="Toggle display of the Posing panel"
    )
    
    bpy.utils.register_class(VIEW3D_PT_RigBotPanel)
    bpy.utils.register_class(BONE_UL_list)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_RigBotPanel)
    bpy.utils.unregister_class(BONE_UL_list)

    properties_to_delete = [
        "rigbot_panel_expanded",
        "rigbot_bone_index",
        "rigbot_constraints_panel_expanded",
        "rigbot_skinning_panel_expanded",
        "rigbot_posing_panel_expanded"
    ]

    for property_name in properties_to_delete:
        try:
            delattr(bpy.types.Scene, property_name)
        except AttributeError:
            pass