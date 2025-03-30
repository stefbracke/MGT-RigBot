import bpy
import bmesh
from mathutils import Vector
from math import cos, sin

def create_cube_shape(name:str, size: float = 1.0) -> bpy.types.Object | None:
    """Creates a wireframe cube mesh object for use as a custom bone shape.
    
    Args:
        name (str): The desired name for the mesh data and object.
        size (float): The overall size of the cube (edge length will be size * 2).

    Returns:
        bpy.types.Object | None: The newly created cube object, or None on failure.
    """
    mesh_data = bpy.data.meshes.new("CTL_" + name)
    if not mesh_data:
        print(f"Failed to create mesh data for '{name}'.")
        return None
    
    bm = bmesh.new()

    verts_coords = [
        Vector((-size, -size, -size)),
        Vector(( size, -size, -size)),
        Vector(( size,  size, -size)),
        Vector((-size,  size, -size)),
        Vector((-size, -size,  size)),
        Vector(( size, -size,  size)),
        Vector(( size,  size,  size)),
        Vector((-size,  size,  size)),
    ]
    verts = [bm.verts.new(coord) for coord in verts_coords]
    edges_indices = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Bottom face
        (4, 5), (5, 6), (6, 7), (7, 4),  # Top face
        (0, 4), (1, 5), (2, 6), (3, 7)   # Connecting edges
    ]
    
    for v1_idx, v2_idx in edges_indices:
        try:
            bm.edges.new((verts[v1_idx], verts[v2_idx]))
        except ValueError:
            pass

    bm.to_mesh(mesh_data)
    bm.free()

    shape_obj = bpy.data.objects.new(name, mesh_data)
    if not shape_obj:
        print(f"Error: Could not create object '{name}'")
        bpy.data.meshes.remove(mesh_data)
        return None
    
    return shape_obj

def create_circle_shape(name:str, radius: float = 1.0, vertices: int = 32) -> bpy.types.Object | None:
    """Creates a wireframe circle mesh object for use as a custom bone shape.
    
    Args:
        name (str): The desired name for the mesh data and object.
        radius (float): The radius of the circle.
        vertices (int): The number of vertices in the circle.

    Returns:
        bpy.types.Object | None: The newly created circle object, or None on failure.
    """
    mesh_data = bpy.data.meshes.new("CTL_" + name)
    if not mesh_data:
        print(f"Failed to create mesh data for '{name}'.")
        return None
    
    bm = bmesh.new()

    # Create vertices in a circular pattern
    verts = []
    num_verts = vertices  # Number of vertices in the circle
    for i in range(num_verts):
        angle = (i / num_verts) * (2 * 3.14159)  # Full circle in radians
        x = radius * cos(angle)
        y = radius * sin(angle)
        verts.append(bm.verts.new((x, y, 0)))

    # Create edges between each pair of vertices
    for i in range(num_verts):
        bm.edges.new((verts[i], verts[(i + 1) % num_verts]))

    bm.to_mesh(mesh_data)
    bm.free()

    shape_obj = bpy.data.objects.new(name, mesh_data)
    if not shape_obj:
        print(f"Error: Could not create object '{name}'")
        bpy.data.meshes.remove(mesh_data)
        return None
    
    return shape_obj

# Function to create a controller of a plane without a face
def create_plane_shape(name:str, size: float = 1.0) -> bpy.types.Object | None:
    """Creates a wireframe plane mesh object for use as a custom bone shape.
    
    Args:
        name (str): The desired name for the mesh data and object.
        size (float): The overall size of the plane (length of each side will be size).

    Returns:
        bpy.types.Object | None: The newly created plane object, or None on failure.
    """
    mesh_data = bpy.data.meshes.new("CTL_" + name)
    if not mesh_data:
        print(f"Failed to create mesh data for '{name}'.")
        return None
    
    bm = bmesh.new()

    # Create vertices for the plane
    verts_coords = [
        Vector((-size / 2, -size / 2, 0)),
        Vector(( size / 2, -size / 2, 0)),
        Vector(( size / 2,  size / 2, 0)),
        Vector((-size / 2,  size / 2, 0)),
    ]
    
    verts = [bm.verts.new(coord) for coord in verts_coords]
    
    # Create edges between each pair of vertices
    edges_indices = [
        (0, 1), (1, 2), (2, 3), (3, 0)   # Plane edges
    ]
    
    for v1_idx, v2_idx in edges_indices:
        try:
            bm.edges.new((verts[v1_idx], verts[v2_idx]))
        except ValueError:
            pass

    bm.to_mesh(mesh_data)
    bm.free()

    shape_obj = bpy.data.objects.new(name, mesh_data)
    if not shape_obj:
        print(f"Error: Could not create object '{name}'")
        bpy.data.meshes.remove(mesh_data)
        return None
    
    return shape_obj