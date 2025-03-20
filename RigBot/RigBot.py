import bpy

# Operator to add an initial bone and enter Edit Mode
class OBJECT_OT_add_initial_bone(bpy.types.Operator):
    bl_idname = "object.add_initial_bone"
    bl_label = "Add Initial Bone"
    bl_description = "Creates an initial bone, sets default viewport display options (including gizmos), and switches to Edit Mode"

    def execute(self, context):
        # If an armature is already active, cancel to avoid errors.
        if context.active_object and context.active_object.type == 'ARMATURE':
            self.report({'WARNING'}, "An armature is already active. Deselect it to add a new initial bone.")
            return {'CANCELLED'}
        bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
        obj = context.active_object
        if obj and obj.type == 'ARMATURE':
            # Set default viewport display options for the armature.
            obj.data.show_axes = True
            obj.data.show_names = True
            obj.show_in_front = True
        # Set the 3D View gizmo properties for object translate and rotate if available.
        if context.space_data:
            context.space_data.show_gizmo_object_translate = True
            context.space_data.show_gizmo_object_rotate = True
        self.report({'INFO'}, "Initial bone added with viewport display options and gizmos enabled, and Edit Mode activated")
        return {'FINISHED'}

# Custom UIList to display bones in a list-like (Outliner) view with parent info
class BONE_UL_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # 'item' is a bone (bpy.types.Bone)
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # Use a row with an operator to select the bone directly
            row = layout.row(align=True)
            select_op = row.operator("object.select_bone", text=item.name, emboss=False)
            select_op.bone_name = item.name  # Pass the bone name to the operator
            if item.parent:
                # Display parent's name in a dimmed style.
                row.label(text=f"(Parent: {item.parent.name})", icon='BLANK1')
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon='BONE_DATA')

# Operator to select a bone
class OBJECT_OT_select_bone(bpy.types.Operator):
    bl_idname = "object.select_bone"
    bl_label = "Select Bone"
    bl_description = "Selects the bone in the 3D Viewport"

    bone_name: bpy.props.StringProperty(
            name="Bone Name",
            description="Name of the bone to select"
    )

    def execute(self, context):
        obj = context.active_object
        if not (obj and obj.type == 'ARMATURE'):
            self.report({'WARNING'}, "No active armature found.")
            return {'CANCELLED'}

        armature = obj.data
        # Check if the bone exists in the armature
        if self.bone_name not in armature.bones:
            self.report({'WARNING'}, f"Bone '{self.bone_name}' not found.")
            return {'CANCELLED'}

        # Store the current mode
        current_mode = context.object.mode

        # Select the bone based on the current mode
        if current_mode == 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')  # Ensure Edit Mode
            for bone in armature.edit_bones:
                bone.select = False
            armature.edit_bones[self.bone_name].select = True
        elif current_mode == 'POSE':
            bpy.ops.object.mode_set(mode='POSE')  # Ensure Pose Mode
            for bone in armature.bones:
                bone.select = False
            armature.bones[self.bone_name].select = True
        else:
            self.report({'WARNING'}, f"Unsupported mode: {current_mode}")
            return {'CANCELLED'}

        # Restore the previous mode
        bpy.ops.object.mode_set(mode=current_mode)
        return {'FINISHED'}

# Operator to rename a bone (popup for new name)
class OBJECT_OT_rename_bone(bpy.types.Operator):
    bl_idname = "object.rename_bone"
    bl_label = "Rename Bone"
    bl_description = "Rename the selected bone."

    bone_name: bpy.props.StringProperty(
            name="Current Bone Name",
            description="Name of the bone to rename"
    )
    new_name: bpy.props.StringProperty(
            name="New Bone Name",
            description="New name for the bone"
    )

    def invoke(self, context, event):
        # Invoke a popup dialog to enter the new name.
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        obj = context.active_object
        if not (obj and obj.type == 'ARMATURE'):
            self.report({'WARNING'}, "No active armature found.")
            return {'CANCELLED'}
        armature = obj.data
        # Ensure we are in Edit Mode so we can rename via edit_bones.
        if obj.mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')
        if self.bone_name not in armature.edit_bones:
            self.report({'WARNING'}, f"Bone '{self.bone_name}' not found in Edit Mode.")
            return {'CANCELLED'}
        # Rename the bone in edit_bones.
        armature.edit_bones[self.bone_name].name = self.new_name
        self.report({'INFO'}, f"Bone renamed to '{self.new_name}'.")
        
        return {'FINISHED'}

# Panel for RigBot UI (foldable)
class VIEW3D_PT_RigBotPanel(bpy.types.Panel):
    bl_label = "RigBot"
    bl_idname = "VIEW3D_PT_RigBotPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RigBot"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Main header row for Skeleton Creation panel
        header_row = layout.row(align=True)
        arrow_icon = 'TRIA_DOWN' if scene.rigbot_panel_expanded else 'TRIA_RIGHT'
        header_row.prop(scene, "rigbot_panel_expanded", text="", icon=arrow_icon, emboss=False)
        header_row.label(text="Skeleton Creation", icon='ARMATURE_DATA')

        # Draw Skeleton Creation content only if expanded
        if scene.rigbot_panel_expanded:
            # Section: Bone Creation (only visible if no armature is active)
            if not (context.active_object and context.active_object.type == 'ARMATURE'):
                box = layout.box()
                box.label(text="Bone Creation", icon='OUTLINER_OB_ARMATURE')
                col = box.column(align=True)
                col.operator("object.add_initial_bone", text="Add Initial Bone", icon='BONE_DATA')
                col.label(text="Creates an initial bone.", icon='INFO')

            # Section: Bone List (Outliner View using UIList)
            layout.separator()
            box = layout.box()
            box.label(text="Bone List", icon='BONE_DATA')
            if context.active_object and context.active_object.type == 'ARMATURE':
                box.template_list("BONE_UL_list", "", context.active_object.data, "bones", scene, "rigbot_bone_index", rows=5)
                # Rename button for the active bone
                if 0 <= scene.rigbot_bone_index < len(context.active_object.data.bones):
                    active_bone = context.active_object.data.bones[scene.rigbot_bone_index]
                    rename_op = box.operator("object.rename_bone", text="Rename Bone")
                    rename_op.bone_name = active_bone.name
            else:
                box.label(text="No active armature.", icon='ERROR')



        # New Section: Controller Creation (expandable)
        ctrl_header = layout.row(align=True)
        ctrl_arrow_icon = 'TRIA_DOWN' if scene.rigbot_ctrl_panel_expanded else 'TRIA_RIGHT'
        ctrl_header.prop(scene, "rigbot_ctrl_panel_expanded", text="", icon=ctrl_arrow_icon, emboss=False)
        ctrl_header.label(text="Controller Creation", icon='DRIVER')
        if scene.rigbot_ctrl_panel_expanded:
            ctrl_box = layout.box()
            ctrl_box.label(text="Controller Creation options will go here.", icon='INFO')
        layout.separator()
        layout.label(text="Hover over elements for tooltips.", icon='QUESTION')

        # Section: Viewport Display Options (collapsible)
        layout.separator()
        box = layout.box()
        row = box.row(align=True)
        arrow_icon_vp = 'TRIA_DOWN' if scene.rigbot_vp_display_expanded else 'TRIA_RIGHT'
        row.prop(scene, "rigbot_vp_display_expanded", text="", icon=arrow_icon_vp, emboss=False)
        row.label(text="Viewport Display Options", icon='HIDE_OFF')
        if scene.rigbot_vp_display_expanded:
            if context.active_object and context.active_object.type == 'ARMATURE':
                armature_data = context.active_object.data
                box.prop(armature_data, "display_type", text="Display As")
                box.prop(armature_data, "show_axes", text="Show Axes")
                box.prop(armature_data, "show_names", text="Show Names")
                box.prop(context.active_object, "show_in_front", text="Show In Front")
            else:
                box.label(text="No active armature selected.", icon='ERROR')
            # Options specific to active bone
            box.separator()
            box.label(text="Active Bone Options", icon='BONE_DATA')
            if context.active_bone:
                box.prop(context.active_bone, "roll", text="Bone Roll")
                # Display tail_radius only if display_type is 'ENVELOPE'
                if context.object.data.display_type == 'ENVELOPE':
                    box.prop(context.active_bone, "tail_radius", text="Bone Radius")
            else:
                box.label(text="No bone selected", icon='NONE')
            # Gizmo options header
            box.separator()
            box.label(text="Gizmo Display", icon='ORIENTATION_GIMBAL')
            if context.space_data:
                box.prop(context.space_data, "show_gizmo_object_translate", text="Show Move Gizmo")
        layout.separator()

# Registration
def register():
    bpy.types.Scene.rigbot_panel_expanded = bpy.props.BoolProperty(
            name="Expand RigBot Panel", default=True,
            description="Toggle display of the RigBot panel"
    )
    bpy.types.Scene.rigbot_vp_display_expanded = bpy.props.BoolProperty(
            name="Expand Viewport Display Options", default=True,
            description="Toggle display of viewport display options"
    )
    bpy.types.Scene.rigbot_ctrl_panel_expanded = bpy.props.BoolProperty(
            name="Expand Controller Creation", default=True,
            description="Toggle display of Controller Creation options"
    )
    bpy.types.Scene.rigbot_bone_index = bpy.props.IntProperty(
            name="Bone Index", default=0,
            description="Active bone index in the RigBot Bone List"
    )
    bpy.utils.register_class(OBJECT_OT_add_initial_bone)
    bpy.utils.register_class(BONE_UL_list)
    bpy.utils.register_class(OBJECT_OT_select_bone)
    bpy.utils.register_class(OBJECT_OT_rename_bone)
    bpy.utils.register_class(VIEW3D_PT_RigBotPanel)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_RigBotPanel)
    bpy.utils.unregister_class(OBJECT_OT_rename_bone)
    bpy.utils.unregister_class(OBJECT_OT_select_bone)
    bpy.utils.unregister_class(BONE_UL_list)
    bpy.utils.unregister_class(OBJECT_OT_add_initial_bone)
    del bpy.types.Scene.rigbot_panel_expanded
    del bpy.types.Scene.rigbot_vp_display_expanded
    del bpy.types.Scene.rigbot_ctrl_panel_expanded
    del bpy.types.Scene.rigbot_bone_index

if __name__ == "__main__":
    register()