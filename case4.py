import bpy
import bmesh
import math

SEGMENTS=64

# Clear scene
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

for i in range(3):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=3.5,      # Adjust hole size
        depth=4,       # Make it tall enough to go through
        location=(i*10, 0, 0)
    )
    button = bpy.context.active_object
    # Round the corners
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bevel(offset=0.75, segments=SEGMENTS)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    
    
