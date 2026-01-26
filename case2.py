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
outer.scale = (1, 1.5, 0.7)  # Make it egg-shaped (taller)
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
    if v.co.z > 30*0.55:
        v.co.z = 30*0.55

bmesh.update_edit_mesh(outer.data)





######################## inner

bpy.ops.object.mode_set(mode='OBJECT')

# Create inner sphere (slightly smaller for wall thickness)
bpy.ops.mesh.primitive_uv_sphere_add(radius=32, segments=SEGMENTS, ring_count=RING_COUNT)
inner = bpy.context.active_object
inner.name = "Inner_Shell"
inner.scale = (1, 1.5, 0.7)  # Match the egg shape
bpy.ops.object.transform_apply(scale=True)

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='DESELECT')

mesh = bmesh.from_edit_mesh(inner.data)

# Select one side
for v in mesh.verts:
    if v.co.y < 28*-0.9:
        v.select = True

bmesh.update_edit_mesh(inner.data)

# Scale to 0 along X axis (flattens to a plane)
bpy.ops.transform.resize(
    value=(0.9, 0, 0.9),
    orient_type='GLOBAL',
    constraint_axis=(True, True, True)
)

# Smooth the sharp transition
bpy.ops.mesh.vertices_smooth(factor=1, repeat=REPEAT)

bpy.ops.mesh.select_all(action='DESELECT')
mesh = bmesh.from_edit_mesh(inner.data)

# Select one side
for v in mesh.verts:
    if v.co.z > 28*0.50:
        v.co.z = 28*0.50

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
    size=30,
    location=(0, 30*0.1, 30*0.5)  # Position on front face
)
screen_hole = bpy.context.active_object
bpy.ops.object.transform_apply(scale=True)
# Round the corners (optional)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.bevel(offset=30*0.05, segments=4)
bpy.ops.object.mode_set(mode='OBJECT')

# Apply boolean
bpy.context.view_layer.objects.active = outer
modifier = outer.modifiers.new(name="Screen", type='BOOLEAN')
modifier.operation = 'DIFFERENCE'
modifier.object = screen_hole

bpy.ops.object.modifier_apply(modifier="Screen")
bpy.data.objects.remove(screen_hole, do_unlink=True)

bpy.ops.object.mode_set(mode='OBJECT')


# Assuming you already have 'outer' shell created

# USB-C port dimensions (in mm, adjust scale as needed)
# Typical USB-C: 8.4mm wide × 2.6mm tall
# We'll make it slightly larger for easy insertion: 9mm × 3mm

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 30*-1.1, 30*0.04),
    scale = (8.5, 30, 2.6)
)
usbc_hole = bpy.context.active_object
bpy.ops.object.transform_apply(scale=True)

# Round the corners for USB-C shape
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.bevel(offset=30*0.015, segments=4)  # Rounded corners
bpy.ops.object.mode_set(mode='OBJECT')

# Cut the hole
bpy.context.view_layer.objects.active = outer
modifier = outer.modifiers.new(name="USBC", type='BOOLEAN')
modifier.operation = 'DIFFERENCE'
modifier.object = usbc_hole
bpy.ops.object.modifier_apply(modifier="USBC")
bpy.data.objects.remove(usbc_hole, do_unlink=True)



bpy.ops.object.mode_set(mode='OBJECT')

# Assuming you already have your egg shape created as 'outer'
# Create a cylinder to punch through for the hole
bpy.ops.mesh.primitive_cylinder_add(
    radius=3.5,      # Adjust hole size
    depth=30,       # Make it tall enough to go through
    location=(0, 30*-1, 30*0.5)  # Position at top of egg
)
hole_cutter = bpy.context.active_object

# Apply boolean difference
bpy.context.view_layer.objects.active = outer
modifier = outer.modifiers.new(name="A", type='BOOLEAN')
modifier.operation = 'DIFFERENCE'
modifier.object = hole_cutter
modifier.solver = 'EXACT'

# Apply the modifier
bpy.ops.object.modifier_apply(modifier="A")

# Delete the cutter object
bpy.data.objects.remove(hole_cutter, do_unlink=True)




bpy.ops.object.mode_set(mode='OBJECT')

# Assuming you already have your egg shape created as 'outer'
# Create a cylinder to punch through for the hole
bpy.ops.mesh.primitive_cylinder_add(
    radius=3.5,      # Adjust hole size
    depth=30,       # Make it tall enough to go through
    location=(30*-0.35, 30*-0.7, 30*0.55)  # Position at top of egg
)
hole_cutter = bpy.context.active_object

# Apply boolean difference
bpy.context.view_layer.objects.active = outer
modifier = outer.modifiers.new(name="B", type='BOOLEAN')
modifier.operation = 'DIFFERENCE'
modifier.object = hole_cutter
modifier.solver = 'EXACT'

# Apply the modifier
bpy.ops.object.modifier_apply(modifier="B")

# Delete the cutter object
bpy.data.objects.remove(hole_cutter, do_unlink=True)




bpy.ops.object.mode_set(mode='OBJECT')

# Assuming you already have your egg shape created as 'outer'
# Create a cylinder to punch through for the hole
bpy.ops.mesh.primitive_cylinder_add(
    radius=3.5,      # Adjust hole size
    depth=30,       # Make it tall enough to go through
    location=(30*0.35, 30*-0.7, 30*0.55)  # Position at top of egg
)
hole_cutter = bpy.context.active_object

# Apply boolean difference
bpy.context.view_layer.objects.active = outer
modifier = outer.modifiers.new(name="C", type='BOOLEAN')
modifier.operation = 'DIFFERENCE'
modifier.object = hole_cutter
modifier.solver = 'EXACT'

# Apply the modifier
bpy.ops.object.modifier_apply(modifier="C")

# Delete the cutter object
bpy.data.objects.remove(hole_cutter, do_unlink=True)


############### venting
import math


for i in range(3):
    bpy.ops.mesh.primitive_cube_add(
        size=30,
        location=(30*(0.2+0.1*i), 30*-1.1, 30*0.22),
        scale = (0.25, 0.6, 0.03),
        rotation=(
            math.radians(0),   # X: 45°
            math.radians(35),    # Y: 0°
            math.radians(0)    # Z: 90°
        )
    )
    usbc_hole = bpy.context.active_object
    
    # Round the corners for USB-C shape
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bevel(offset=30*0.015, segments=4)  # Rounded corners
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Cut the hole
    bpy.context.view_layer.objects.active = outer
    modifier = outer.modifiers.new(name="vent", type='BOOLEAN')
    modifier.operation = 'DIFFERENCE'
    modifier.object = usbc_hole
    bpy.ops.object.modifier_apply(modifier="vent")
    bpy.data.objects.remove(usbc_hole, do_unlink=True)


for i in range(3):
    bpy.ops.mesh.primitive_cube_add(
        size=30,
        location=(30*(-0.2-0.1*i), 30*-1.1, 30*0.22),
        scale = (0.25, 0.6, 0.03),
        rotation=(
            math.radians(0),   # X: 45°
            math.radians(-35),    # Y: 0°
            math.radians(0)    # Z: 90°
        )
    )
    usbc_hole = bpy.context.active_object
    
    # Round the corners for USB-C shape
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bevel(offset=30*0.015, segments=4)  # Rounded corners
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Cut the hole
    bpy.context.view_layer.objects.active = outer
    modifier = outer.modifiers.new(name="vent", type='BOOLEAN')
    modifier.operation = 'DIFFERENCE'
    modifier.object = usbc_hole
    bpy.ops.object.modifier_apply(modifier="vent")
    bpy.data.objects.remove(usbc_hole, do_unlink=True)
