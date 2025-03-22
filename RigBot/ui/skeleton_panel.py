import bpy

class VIEW3D_PT_SkeletonCreationPanel(bpy.types.Panel):
    bl_label = "Skeleton Creation"
    bl_idname = "VIEW3D_PT_SkeletonCreationPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RigBot"
    bl_parent_id = "VIEW3D_PT_RigBotPanel"

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

def register():
    bpy.types.Scene.rigbot_panel_expanded = bpy.props.BoolProperty(
            name="Expand RigBot Panel", default=True,
            description="Toggle display of the RigBot panel"
    )
    bpy.types.Scene.rigbot_bone_index = bpy.props.IntProperty(
            name="Bone Index", default=0,
            description="Active bone index in the RigBot Bone List"
    )
    bpy.utils.register_class(VIEW3D_PT_SkeletonCreationPanel)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_SkeletonCreationPanel)
    del bpy.types.Scene.rigbot_panel_expanded
    del bpy.types.Scene.rigbot_bone_index