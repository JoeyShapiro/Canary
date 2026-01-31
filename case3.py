import bpy
import bmesh

SEGMENTS=64
RING_COUNT=32
REPEAT=5
if True: # Production
    SEGMENTS=256
    RING_COUNT=128
    REPEAT=50

# Clear scene
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create outer egg shape (UV sphere scaled vertically)
bpy.ops.mesh.primitive_uv_sphere_add(radius=34, segments=SEGMENTS, ring_count=RING_COUNT)
outer = bpy.context.active_object
outer.name = "Outer_Shell"
outer.scale = (1.0, 1.55, 0.3)  # Make it egg-shaped (taller)
bpy.ops.object.transform_apply(scale=True)



bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='DESELECT')

mesh = bmesh.from_edit_mesh(outer.data)

# Select one side
for v in mesh.verts:
    if v.co.y < 30*-0.9:
        v.select = True

bmesh.update_edit_mesh(outer.data)

# Scale to 0 along X axis (flattens to a plane)
bpy.ops.transform.resize(
    value=(0.9, 0, 0.9),
    orient_type='GLOBAL',
    constraint_axis=(True, True, True) # not sure what this does
)

# Smooth the sharp transition
bpy.ops.mesh.vertices_smooth(factor=1, repeat=REPEAT)

bpy.ops.mesh.select_all(action='DESELECT')

mesh = bmesh.from_edit_mesh(outer.data)

# Select one side
for v in mesh.verts:
    if v.co.z > 9:
        v.co.z = 9

bmesh.update_edit_mesh(outer.data)

# Now cut it in half to make two halves
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')

bpy.ops.mesh.bisect(
    plane_co=(0, 0, 0),
    plane_no=(0, 0, 1),
    clear_inner=True,
    clear_outer=False,
    use_fill=True
)




#bpy.ops.object.mode_set(mode='OBJECT')

#bpy.ops.mesh.primitive_cylinder_add(
#    radius=3.6,      # Adjust hole size
#    depth=4,       # Make it tall enough to go through
#    location=(0, -50, 0)  # Position at top of egg
#)
#screen_hole = bpy.context.active_object
## Round the corners
#bpy.ops.object.mode_set(mode='EDIT')
#bpy.ops.mesh.select_all(action='SELECT')
#bpy.ops.mesh.bevel(offset=0.5, segments=SEGMENTS)
#bpy.ops.object.mode_set(mode='EDIT')
#bpy.ops.mesh.select_all(action='SELECT')

#bpy.ops.mesh.bisect(
#    plane_co=(0, 0, 0),
#    plane_no=(0, 0, 1),
#    clear_inner=True,
#    clear_outer=False,
#    use_fill=True
#)
#bpy.ops.object.mode_set(mode='OBJECT')

#bpy.ops.mesh.primitive_cylinder_add(
#    radius=3.6,      # Adjust hole size
#    depth=4,       # Make it tall enough to go through
#    location=(-10, -50, 0)  # Position at top of egg
#)
## Round the corners
#bpy.ops.object.mode_set(mode='EDIT')
#bpy.ops.mesh.select_all(action='SELECT')
#bpy.ops.mesh.bevel(offset=0.25, segments=SEGMENTS)
#bpy.ops.object.mode_set(mode='EDIT')
#bpy.ops.mesh.select_all(action='SELECT')

#bpy.ops.mesh.bisect(
#    plane_co=(0, 0, 0),
#    plane_no=(0, 0, 1),
#    clear_inner=True,
#    clear_outer=False,
#    use_fill=True
#)
#bpy.ops.object.mode_set(mode='OBJECT')

#bpy.ops.mesh.primitive_cylinder_add(
#    radius=3.6,      # Adjust hole size
#    depth=4,       # Make it tall enough to go through
#    location=(10, -50, 0)  # Position at top of egg
#)
## Round the corners
#bpy.ops.object.mode_set(mode='EDIT')
#bpy.ops.mesh.select_all(action='SELECT')
#bpy.ops.mesh.bevel(offset=0.75, segments=SEGMENTS)
#bpy.ops.object.mode_set(mode='EDIT')
#bpy.ops.mesh.select_all(action='SELECT')

#bpy.ops.mesh.bisect(
#    plane_co=(0, 0, 0),
#    plane_no=(0, 0, 1),
#    clear_inner=True,
#    clear_outer=False,
#    use_fill=True
#)
bpy.ops.object.mode_set(mode='OBJECT')


def clean_mesh_for_printing(obj):
    """Clean up mesh to be manifold (3D printable)"""
    
    # Make sure object is active
    bpy.context.view_layer.objects.active = obj
    
    # Enter edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Select all
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Remove doubles (merge by distance)
    bpy.ops.mesh.remove_doubles(threshold=0.0001)  # 0.1mm tolerance
    
    # Recalculate normals (fix inside-out faces)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    
    # Select non-manifold geometry to check
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_non_manifold()
    
    # Get the count
    mesh = bmesh.from_edit_mesh(obj.data)
    non_manifold_count = sum(1 for e in mesh.edges if e.select)
    
    if non_manifold_count > 0:
        print(f"Warning: {non_manifold_count} non-manifold edges remain")
        
        # Try to fix common issues
        bpy.ops.mesh.select_all(action='SELECT')
        
        # Fill holes
        bpy.ops.mesh.fill_holes(sides=0)
        
        # Delete loose geometry
        bpy.ops.mesh.delete_loose()
        
        # Dissolve degenerate faces
        bpy.ops.mesh.dissolve_degenerate()
    else:
        print("Mesh is manifold (3D printable)!")
    
    # Back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return non_manifold_count

# Use it on your object
clean_mesh_for_printing(outer)
