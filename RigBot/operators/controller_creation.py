import bpy
from bpy.props import StringProperty, FloatVectorProperty

class OBJECT_OT_place_controller(bpy.types.Operator):
    bl_idname = "object.place_controller"
    bl_label = "Place Controller"
    bl_description = "Places a controller shape at the location of the selected bone"

    def execute(self, context):
        obj = context.active_object
        scene = context.scene

        if not (obj and obj.type == 'ARMATURE' and context.mode == 'EDIT_ARMATURE' and context.active_bone):
            self.report({'WARNING'}, "Please select a bone in Edit Mode of an Armature.")
            return {'CANCELLED'}

        selected_bone = context.active_bone
        shape_type = scene.rigbot_controller_shape
        color = scene.rigbot_controller_color

        # Create the controller object based on the selected shape
        if shape_type == 'BOX':
            bpy.ops.mesh.primitive_cube_add(location=selected_bone.head)
            controller = context.active_object
        elif shape_type == 'CIRCLE':
            bpy.ops.curve.primitive_bezier_circle_add(location=selected_bone.head)
            controller = context.active_object
        elif shape_type == 'SQUARE':
            bpy.ops.mesh.primitive_plane_add(location=selected_bone.head)
            controller = context.active_object
            # Rotate the plane to face upwards (optional)
            controller.rotation_euler = (1.5708, 0, 0) # 90 degrees in X
        else:
            self.report({'WARNING'}, "Invalid controller shape selected.")
            return {'CANCELLED'}

        controller.name = f"{selected_bone.name}_CTRL" # Basic naming

        # Set the color of the controller (basic method using material)
        mat = bpy.data.materials.new(name=f"{controller.name}_Mat")
        mat.use_nodes = True
        principled_bsdf = mat.node_tree.nodes["Principled BSDF"]
        principled_bsdf.inputs["Base Color"].default_value = (color[0], color[1], color[2], 1)
        if controller.type == 'MESH':
            controller.data.materials.append(mat)
        elif controller.type == 'CURVE':
            controller.data.materials.append(mat) # May need different approach for curves

        self.report({'INFO'}, f"Controller '{controller.name}' created for bone '{selected_bone.name}'.")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_OT_place_controller)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_place_controller)