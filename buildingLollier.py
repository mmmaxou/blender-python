import bpy
import random
import bmesh


def createBuilding(x, y, size, pixel):
    print("Creating building")
    # Create a cube
    
    # Create a cube
    bpy.ops.mesh.primitive_cube_add(radius=size, location=(x, y, 0))    

    # Use a material
    activeObject = bpy.context.active_object
    mat = bpy.data.materials.get("Building")
    activeObject.data.materials.append(mat)
    #bpy.context.object.active_material.diffuse_color = [k / 255 for k in pixel]

    # Modifier le cube
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(bpy.context.object.data)
    bm.faces.ensure_lookup_table()
    
    # Define the modifiers
    scale_Z = 1.6
    padding = 0.1
    height_scaler = 7
    h = size*(2-scale_Z)


    # Extrude TOP
    bpy.ops.mesh.select_all(action="DESELECT")
    bm.faces[5].select = True
    r = random.uniform(size/height_scaler, size*height_scaler*0.6)
    bpy.ops.transform.translate(value = (0, 0, r))
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, padding)}) 


    
    #création faces milieu


    bpy.ops.mesh.select_all(action="DESELECT")
    bm.faces.ensure_lookup_table()
    bm.faces[6].select = True
    r = random.uniform( (size/height_scaler) *0.3 , size*height_scaler*0.0001)
    bpy.ops.transform.translate(value = (0, 0, r))
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, padding)}) 


    bpy.ops.mesh.select_all(action="DESELECT")
    bm.faces.ensure_lookup_table()
    bm.faces[10].select = True
    r = random.uniform( (size/height_scaler) , size*height_scaler * 0.001)
    bpy.ops.transform.translate(value = (0, 0, r))
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, padding)}) 

    bpy.ops.mesh.select_all(action="DESELECT")
    bm.faces.ensure_lookup_table()
    bm.faces[14].select = True
    r = random.uniform( (size/height_scaler) , size*height_scaler *0.1 )
    bpy.ops.transform.translate(value = (0, 0, r))
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, padding)}) 



    #renfoncement milieu
    bpy.ops.mesh.select_all(action="DESELECT")
    bm.faces.ensure_lookup_table()
    bm.faces[5].select = True
    bm.faces[7].select = True
    bm.faces[8].select = True
    bm.faces[9].select = True
    renfoncementR = random.uniform(0.6,0.85);
    bpy.ops.transform.resize(value = (renfoncementR,renfoncementR,renfoncementR))



    #bpy.ops.mesh.select_all(action="DESELECT")
    #bm.faces.ensure_lookup_table()
    #bm.faces[14].select = True
    #bm.faces[19].select = True
    #bm.faces[20].select = True
    #bm.faces[21].select = True
    #renfoncementR = random.uniform(0.6,1);
    #bpy.ops.transform.resize(value = (renfoncementR,renfoncementR,renfoncementR))



    # bm.faces[5].select=True
    # bpy.ops.transform.rotate(value = 0.3, axis = (0, 1, 0))
    

    # bpy.ops.mesh.select_all(action="DESELECT")

    # bm.faces[0].select=True
    # bm.faces[2].select=True
    # bm.faces[4].select=True

    # bpy.ops.mesh.bevel(offset=0.12817)
    # bpy.ops.object.editmode_toggle()


    # Define the modifiers
    scale_Z = 1.6
    padding = 0.1
    amount  = 10

   #bevel 


    #Select all and duplicate
    

    bpy.ops.object.mode_set(mode='OBJECT')


# 1 -> 