import bpy

def create_cube_controller(name="Faceless_Cube_Controller", size=1.0):
    """Creates a cube object."""
    half_size = size / 2.0
    verts = [
        (-half_size, -half_size, -half_size), ( half_size, -half_size, -half_size),
        ( half_size,  half_size, -half_size), (-half_size,  half_size, -half_size),
        (-half_size, -half_size,  half_size), ( half_size, -half_size,  half_size),
        ( half_size,  half_size,  half_size), (-half_size,  half_size,  half_size)
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6),
        (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)
    ]
    faces = []

    mesh_data = bpy.data.meshes.new("CTL_" + name)
    mesh_data.from_pydata(verts, edges, faces)
    mesh_data.update()

    obj = bpy.data.objects.new(name, mesh_data)
    return obj

# def create_other_shape(name="Other_Shape", ...):
#     """Creates another control shape."""
#     # ... vertex, edge, face definitions ...
#     # ... mesh and object creation ...
#     return obj

# Add more functions for other shapes...