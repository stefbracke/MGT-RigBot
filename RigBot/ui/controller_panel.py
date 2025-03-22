import bpy

class VIEW3D_PT_ControllerCreationPanel(bpy.types.Panel):
    bl_label = "Controller Creation"
    bl_idname = "VIEW3D_PT_ControllerCreationPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RigBot"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Header row for Controller Creation panel
        header_row = layout.row(align=True)
        arrow_icon = 'TRIA_DOWN' if scene.rigbot_ctrl_panel_expanded else 'TRIA_RIGHT'
        header_row.prop(scene, "rigbot_ctrl_panel_expanded", text="", icon=arrow_icon, emboss=False)
        header_row.label(text="Controller Creation Options", icon='DRIVER')

        # Draw Controller Creation content only if expanded
        if scene.rigbot_ctrl_panel_expanded:
            box = layout.box()
            box.label(text="Controller Creation Options", icon='INFO')
            # Add your controller creation operators and properties here
            # Example:
            # box.operator("object.create_controller", text="Create Controller", icon='CONSTRAINT')

def register():
    bpy.types.Scene.rigbot_ctrl_panel_expanded = bpy.props.BoolProperty(
            name="Expand Controller Panel", default=True, # You might need to add this property definition in your __init__.py or controller_panel.py
            description="Toggle display of controller creation options"
    )
    bpy.utils.register_class(VIEW3D_PT_ControllerCreationPanel)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_ControllerCreationPanel)
    del bpy.types.Scene.rigbot_ctrl_panel_expanded
