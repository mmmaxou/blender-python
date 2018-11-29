import bpy
import random
import bmesh


def createFlat(x, y, size, pixel):
    # Create a cube
    obj = bpy.ops.mesh.primitive_cube_add(radius=size, location=(x, y, 0))

    # Create a material
    activeObject = bpy.context.active_object
    mat = bpy.data.materials.new(name="MaterialName")
    activeObject.data.materials.append(mat)
    bpy.context.object.active_material.diffuse_color = [k / 255 for k in pixel]

    # Modifier le cube
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action="DESELECT")
    bm = bmesh.from_edit_mesh(bpy.context.object.data)
    bm.faces.ensure_lookup_table()
    
    # Define the modifiers
    scale_Z = 1.6
    padding = 0.1
    amount  = 10

    # Reduce size
    bm.faces[5].select = True
    bpy.ops.transform.translate(value = (0, 0, -size*scale_Z))
    h = size*(2-scale_Z)

    # Select all and duplicate
    bpy.ops.mesh.select_all(action='SELECT')
    for i in range(amount):
        bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1}, TRANSFORM_OT_translate={"value":(0, 0, h+padding)})
    bpy.ops.object.mode_set(mode='OBJECT')


# 1 -> 