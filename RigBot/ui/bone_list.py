import bpy

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
    bpy.utils.register_class(BONE_UL_list)

def unregister():
    bpy.utils.unregister_class(BONE_UL_list)