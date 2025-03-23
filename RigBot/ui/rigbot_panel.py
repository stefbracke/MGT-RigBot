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

        # Skeleton Creation Panel
        # Main header row for Skeleton Creation panel
        header_row_skeleton = layout.row(align=True)
        arrow_icon_skeleton = 'TRIA_DOWN' if scene.rigbot_panel_expanded else 'TRIA_RIGHT'
        header_row_skeleton.prop(scene, "rigbot_panel_expanded", text="", icon=arrow_icon_skeleton, emboss=False)
        header_row_skeleton.label(text="Skeleton Creation", icon='ARMATURE_DATA')

        # Draw Skeleton Creation content only if expanded
        if scene.rigbot_panel_expanded:
            # Section: Bone Creation (only visible if no armature is active)
            if not (context.active_object and context.active_object.type == 'ARMATURE'):
                box = layout.box()
                box.label(text="Bone Creation", icon='OUTLINER_OB_ARMATURE')
                col = box.column(align=True)
                col.operator("object.add_initial_bone", text="Add Initial Bone", icon='BONE_DATA')

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

        layout.separator()

        # Controller Creation Panel
        # Header row for Controller Creation panel
        header_row_controller = layout.row(align=True)
        arrow_icon_controller = 'TRIA_DOWN' if scene.rigbot_ctrl_panel_expanded else 'TRIA_RIGHT'
        header_row_controller.prop(scene, "rigbot_ctrl_panel_expanded", text="", icon=arrow_icon_controller, emboss=False)
        header_row_controller.label(text="Controller Creation Options", icon='DRIVER')

        # Draw Controller Creation content only if expanded
        if scene.rigbot_ctrl_panel_expanded:
            box = layout.box()
            box.label(text="Controller Options", icon='INFO')
            col = box.column(align=True)
            col.prop(scene, "rigbot_controller_shape")
            col.prop(scene, "rigbot_controller_color", text="") # Text is empty as the label is "Controller Color"
            col.operator("object.place_controller", text="Place Controller")
            
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
            name="Bone Index", default=0,
            description="Active bone index in the RigBot Bone List"
    )
    bpy.types.Scene.rigbot_ctrl_panel_expanded = bpy.props.BoolProperty(
            name="Expand Controller Panel", default=True,
            description="Toggle display of controller creation options"
    )
    bpy.types.Scene.rigbot_controller_shape = bpy.props.EnumProperty(
            items=[
                ('BOX', "Box", "Create a box controller"),
                ('CIRCLE', "Circle", "Create a circle controller"),
                ('SQUARE', "Square", "Create a square controller"),
            ],
            name="Controller Shape",
            default='CIRCLE',
            description="Shape of the controller to create"
    )
    bpy.types.Scene.rigbot_controller_color = bpy.props.FloatVectorProperty(
            name="Controller Color",
            subtype='COLOR',
            default=(0.8, 0.2, 0.2),  # Default to red
            min=0.0, max=1.0,
            description="Color of the controller"
    )
    bpy.utils.register_class(VIEW3D_PT_RigBotPanel)
    bpy.utils.register_class(BONE_UL_list)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_RigBotPanel)
    bpy.utils.unregister_class(BONE_UL_list)
    del bpy.types.Scene.rigbot_panel_expanded
    del bpy.types.Scene.rigbot_bone_index
    del bpy.types.Scene.rigbot_ctrl_panel_expanded
    del bpy.types.Scene.rigbot_controller_shape
    del bpy.types.Scene.rigbot_controller_color