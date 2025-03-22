import bpy

class VIEW3D_PT_ViewportDisplayPanel(bpy.types.Panel):
    bl_label = "Viewport Display Options"
    bl_idname = "VIEW3D_PT_ViewportDisplayPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RigBot"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.active_object
        arm_data = obj.data if obj and obj.type == 'ARMATURE' else None
        active_bone = context.active_bone

        box = layout.box()
        row = box.row(align=True)
        arrow_icon_vp = 'TRIA_DOWN' if scene.rigbot_vp_display_expanded else 'TRIA_RIGHT'
        row.prop(scene, "rigbot_vp_display_expanded", text="", icon=arrow_icon_vp, emboss=False)
        row.label(text="Viewport Display Options", icon='HIDE_OFF') 
        
        if not scene.rigbot_vp_display_expanded:
            return
            
        if arm_data:
            box.prop(arm_data, "display_type", text="Display As")
            box.prop(arm_data, "show_axes", text="Show Axes")
            box.prop(arm_data, "show_names", text="Show Names")
            box.prop(obj, "show_in_front", text="Show In Front")
        else:
            box.label(text="No active armature selected.", icon='ERROR')

        # Options specific to active bone
        box.separator()
        box.label(text="Active Bone Options", icon='BONE_DATA')
        if active_bone:
            box.prop(active_bone, "roll", text="Bone Roll")
            # Display tail_radius only if display_type is 'ENVELOPE'
            if getattr(arm_data, "display_type", None) == 'ENVELOPE':
                box.prop(active_bone, "tail_radius", text="Bone Radius")
        else:
            box.label(text="No bone selected", icon='BLANK1')

        # Gizmo options header
        box.separator()
        box.label(text="Gizmo Display", icon='ORIENTATION_GIMBAL')
        if getattr(context.space_data, "show_gizmo_object_translate", None) is not None:
            box.prop(context.space_data, "show_gizmo_object_translate", text="Show Move Gizmo")


def register():
    bpy.types.Scene.rigbot_vp_display_expanded = bpy.props.BoolProperty(
            name="Expand Viewport Display Options", default=True,
            description="Toggle display of viewport display options"
    )
    bpy.utils.register_class(VIEW3D_PT_ViewportDisplayPanel)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_ViewportDisplayPanel)
    del bpy.types.Scene.rigbot_vp_display_expanded