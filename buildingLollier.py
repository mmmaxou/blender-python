import bpy
import random
import bmesh


def createBuilding(x, y, pixel):
    # Create a cube
    obj = bpy.ops.mesh.primitive_cube_add(radius=1, location=(x, y, 0))


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



    bm.faces[5].select=True
    bpy.ops.transform.rotate(value = 0.3, axis = (0, 1, 0))
    

    bpy.ops.mesh.select_all(action="DESELECT")

    bm.faces[0].select=True
    bm.faces[2].select=True
    bm.faces[4].select=True

    bpy.ops.mesh.bevel(offset=0.12817)
    bpy.ops.object.editmode_toggle()


    # Define the modifiers
    scale_Z = 1.6
    padding = 0.1
    amount  = 10

   #bevel 


    #Select all and duplicate
    

    bpy.ops.object.mode_set(mode='OBJECT')


# 1 -> 