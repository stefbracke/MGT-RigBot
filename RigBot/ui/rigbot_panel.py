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

            # Parent to Bone button
            parent_op = col.operator(
                    "object.parent_set",
                    text="Parent to Bone",
                    icon='BONE_DATA' # Or 'CONSTRAINT_BONE' or 'LINKED'
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
            box.label(text="Constraint options placeholder...")
        
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