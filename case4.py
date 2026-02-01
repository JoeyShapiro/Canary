import bpy
import bmesh
import math

SEGMENTS=256

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
    bpy.ops.mesh.bisect(
        plane_co=(0, 0, 0),
        plane_no=(0, 0, 1),
        clear_inner=True,
        clear_outer=False,
        use_fill=True
    )
    bpy.ops.object.mode_set(mode='OBJECT')
    
    if i&1 == 0:
        bpy.ops.mesh.primitive_cone_add(
            vertices=3,      # 4 sides = square pyramid
            radius1=3,       # Base radius (0 = pointed)
            radius2=0,       # Top radius 
            depth=2,        # Height
            location=(i*10, 0, 3-0.4), # whatever, can do lots. best place to intersect
        )
    else:
        bpy.ops.mesh.primitive_cube_add(
            size=3.5,      # 4 sides = square pyramid
            location=(i*10, 0, 4-0.6), # whatever, can do lots. best place to intersect
        )
    
    screen_hole = bpy.context.active_object
    # Round the corners
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.bevel(offset=0.25, segments=4)

    # Apply boolean
    bpy.context.view_layer.objects.active = button
    modifier = button.modifiers.new(name="Screen", type='BOOLEAN')
    modifier.operation = 'DIFFERENCE'
    modifier.object = screen_hole
    modifier.solver = 'EXACT'

    bpy.ops.object.modifier_apply(modifier="Screen")
    bpy.data.objects.remove(screen_hole, do_unlink=True)
