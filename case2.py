import bpy
import bmesh

# Clear scene
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create outer egg shape (UV sphere scaled vertically)
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, segments=64, ring_count=32)
outer = bpy.context.active_object
outer.name = "Outer_Shell"
outer.scale = (1, 1.4, 0.7)  # Make it egg-shaped (taller)
bpy.ops.object.transform_apply(scale=True)



bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='DESELECT')

mesh = bmesh.from_edit_mesh(outer.data)

# Select one side
for v in mesh.verts:
    if v.co.y < -0.9:
        v.select = True

bmesh.update_edit_mesh(outer.data)

# Scale to 0 along X axis (flattens to a plane)
bpy.ops.transform.resize(
    value=(1, 0, 1),
    orient_type='GLOBAL',
    constraint_axis=(False, True, False) # not sure what this does
)

# Smooth the sharp transition
bpy.ops.mesh.vertices_smooth(factor=0.5, repeat=5)

bpy.ops.mesh.select_all(action='DESELECT')

mesh = bmesh.from_edit_mesh(outer.data)

# Select one side
for v in mesh.verts:
    if v.co.z > 0.55:
        v.co.z = 0.55

bmesh.update_edit_mesh(outer.data)





######################## inner

bpy.ops.object.mode_set(mode='OBJECT')

# Create inner sphere (slightly smaller for wall thickness)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.95, segments=64, ring_count=32)
inner = bpy.context.active_object
inner.name = "Inner_Shell"
inner.scale = (1, 1.3, 0.7)  # Match the egg shape
bpy.ops.object.transform_apply(scale=True)

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='DESELECT')

mesh = bmesh.from_edit_mesh(inner.data)

# Select one side
for v in mesh.verts:
    if v.co.y < -0.9:
        v.select = True

bmesh.update_edit_mesh(inner.data)

# Scale to 0 along X axis (flattens to a plane)
bpy.ops.transform.resize(
    value=(1, 0, 1),
    orient_type='GLOBAL',
    constraint_axis=(False, True, False)
)

# Smooth the sharp transition
bpy.ops.mesh.vertices_smooth(factor=0.5, repeat=5)

bpy.ops.mesh.select_all(action='DESELECT')
mesh = bmesh.from_edit_mesh(inner.data)

# Select one side
for v in mesh.verts:
    if v.co.z > 0.50:
        v.co.z = 0.50

bmesh.update_edit_mesh(inner.data)


bpy.ops.object.mode_set(mode='OBJECT')

# Boolean difference to hollow out
modifier = outer.modifiers.new(name="Boolean", type='BOOLEAN')
modifier.operation = 'DIFFERENCE'
modifier.object = inner
modifier.solver = 'EXACT'  # or 'EXACT' for better precision

# Apply the modifier
bpy.context.view_layer.objects.active = outer
bpy.ops.object.modifier_apply(modifier="Boolean")

# Delete the inner sphere (no longer needed)
bpy.data.objects.remove(inner, do_unlink=True)

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




########################## face
bpy.ops.object.mode_set(mode='OBJECT')

# Create a rectangular hole for a screen
bpy.ops.mesh.primitive_cube_add(
    size=2,
    location=(0, 0.1, 0)  # Position on front face
)
screen_hole = bpy.context.active_object
screen_hole.scale = (0.5, 0.5, 1.0)
bpy.ops.object.transform_apply(scale=True)
# Round the corners (optional)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.bevel(offset=0.05, segments=4)
bpy.ops.object.mode_set(mode='OBJECT')

# Apply boolean
bpy.context.view_layer.objects.active = outer
modifier = outer.modifiers.new(name="Screen", type='BOOLEAN')
modifier.operation = 'DIFFERENCE'
modifier.object = screen_hole

bpy.ops.object.modifier_apply(modifier="Screen")
bpy.data.objects.remove(screen_hole, do_unlink=True)

bpy.ops.object.mode_set(mode='OBJECT')
