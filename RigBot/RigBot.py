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

# Dummy operator for placeholder actions
class OBJECT_OT_dummy_operator(bpy.types.Operator):
    bl_idname = "object.dummy_operator"
    bl_label = "Dummy Operator"
    bl_description = "Placeholder operator – no functionality implemented yet."

    def execute(self, context):
        self.report({'INFO'}, "Executed dummy operator")
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

        # Main header row with an arrow toggle and "RigBot" label
        header_row = layout.row(align=True)
        arrow_icon = 'TRIA_DOWN' if scene.rigbot_panel_expanded else 'TRIA_RIGHT'
        header_row.prop(scene, "rigbot_panel_expanded", text="", icon=arrow_icon, emboss=False)
        header_row.label(text="Skeleton Creation", icon='ARMATURE_DATA')

        # Draw the rest of the UI only if the panel is expanded
        if scene.rigbot_panel_expanded:
            # Section: Bone Creation (only visible if no armature is active)
            if not (context.active_object and context.active_object.type == 'ARMATURE'):
                box = layout.box()
                box.label(text="Bone Creation", icon='OUTLINER_OB_ARMATURE')
                col = box.column(align=True)
                col.operator("object.add_initial_bone", text="Add Initial Bone", icon='BONE_DATA')
                col.label(text="Creates an initial bone.", icon='INFO')

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
                # Add header for Gizmo options
                box.separator()
                box.label(text="Gizmo Display", icon='ORIENTATION_GIMBAL')
                if context.space_data:
                    box.prop(context.space_data, "show_gizmo_object_translate", text="Show Move Gizmo")
                    box.prop(context.space_data, "show_gizmo_object_rotate", text="Show Rotate Gizmo")
            layout.separator()
            layout.label(text="Hover over elements for tooltips.", icon='QUESTION')

def register():
    bpy.types.Scene.rigbot_panel_expanded = bpy.props.BoolProperty(
            name="Expand RigBot Panel", default=True,
            description="Toggle display of the RigBot panel"
    )
    bpy.types.Scene.rigbot_vp_display_expanded = bpy.props.BoolProperty(
            name="Expand Viewport Display Options", default=True,
            description="Toggle display of viewport display options"
    )
    bpy.utils.register_class(OBJECT_OT_add_initial_bone)
    bpy.utils.register_class(OBJECT_OT_dummy_operator)
    bpy.utils.register_class(VIEW3D_PT_RigBotPanel)

def unregister():
    del bpy.types.Scene.rigbot_panel_expanded
    del bpy.types.Scene.rigbot_vp_display_expanded
    bpy.utils.unregister_class(VIEW3D_PT_RigBotPanel)
    bpy.utils.unregister_class(OBJECT_OT_dummy_operator)
    bpy.utils.unregister_class(OBJECT_OT_add_initial_bone)

if __name__ == "__main__":
    register()
