import bpy
import random
import bmesh
from math import radians

def createFlat(x, y, size, pixel):
    # Create a cube
    bpy.ops.mesh.primitive_cube_add(radius=size, location=(x, y, 0))

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
    amount = 10

    # Reduce size
    bm.faces[5].select = True
    bpy.ops.transform.translate(value=(0, 0, -size*scale_Z))
    h = size*(2-scale_Z)

    # Select all and duplicate
    bpy.ops.mesh.select_all(action='SELECT')
    for i in range(amount):
        bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode": 1}, TRANSFORM_OT_translate={"value": (0, 0, h+padding)})
    bpy.ops.object.mode_set(mode='OBJECT')


def createBuilding(x, y, size, pixel):
    print("Building creation")
    
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
    r = random.uniform(size/height_scaler, size*height_scaler)
    bpy.ops.transform.translate(value = (0, 0, r))
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, padding)})    
    
    # Move one edge    
    bm.edges.ensure_lookup_table()
    bpy.ops.mesh.select_all(action="DESELECT")
    bm.edges[len(bm.edges)-5-(int(bool(random.getrandbits(1)))*2)].select = True
    r = (int(bool(random.getrandbits(1)))*2)-1
    bpy.ops.transform.translate(value = (0, 0.1*r, 0))

    # Extrude TOP
    bpy.ops.mesh.select_all(action="DESELECT")
    bm.faces.ensure_lookup_table()
    bm.faces[len(bm.faces)-4].select = True
    r = random.uniform(size/height_scaler, size*height_scaler)
    r2 = random.uniform(padding/height_scaler, padding*height_scaler)
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, r)})
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, r2)})    

    for i in range(4):
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, 0.05)})
        bpy.ops.transform.resize(value=(1.05, 1.05, 1.05))
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, 0.05)})
        bpy.ops.transform.resize(value=(1/1.05, 1/1.05, 1/1.05))

    # Move one edge
    bm.edges.ensure_lookup_table()
    bpy.ops.mesh.select_all(action="DESELECT")
    bm.edges[len(bm.edges)-5-(int(bool(random.getrandbits(1)))*2)].select = True
    r = (int(bool(random.getrandbits(1)))*2)-1
    bpy.ops.transform.translate(value = (0, 0.1*r, 0)) 

    # Extrude TOP
    bpy.ops.mesh.select_all(action="DESELECT")
    bm.faces.ensure_lookup_table()
    bm.faces[len(bm.faces)-4].select = True
    r = random.uniform(size/height_scaler, size*height_scaler)
    r2 = random.uniform(padding/height_scaler, padding*height_scaler)
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, r)})
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, r2)})

    top_face_index = save_selection(bm)

    if bool(random.getrandbits(1)):
        bm.faces.ensure_lookup_table()
        bpy.ops.mesh.select_all(action="DESELECT")
        bm.faces[len(bm.faces)-5].select = True
        location = bm.faces[len(bm.faces)-5].calc_center_median()
        print(location)
        bpy.ops.mesh.extrude_region()
        bpy.ops.transform.resize(value=(0.8, 0.8, 0.8))
        if location[0] >= -0.1 and location[0] <= 0.1 and location[1] > 0:
            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, -padding, 0)})
        elif location[0] >= -0.1 and location[0] <= 0.1 and location[1] < 0:
            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, padding, 0)})
        elif location[0] > 0 and location[1] >= -0.1 and location[1] <= 0.1:
            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (-padding, 0, 0)})
        elif location[0] < 0 and location[1] >= -0.1 and location[1] <= 0.1:
            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (padding, 0, 0)})
        bpy.ops.mesh.bevel(offset=padding)
    
    # Reduce TOP
    use_selection(bm, top_face_index)
    bpy.ops.transform.resize(value=(0.85, 0.85, 0.85))

    # Extrude TOP
    r = random.uniform(size/height_scaler, size*height_scaler)
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, r)})
    

    # TOP FLOOR
    for i in range(3):
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, 0.05)})
        bpy.ops.transform.resize(value=(1.05, 1.05, 1.05))
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, 0.05)})
        bpy.ops.transform.resize(value=(1/1.05, 1/1.05, 1/1.05))
    
    r2 = random.uniform(padding/height_scaler, padding*height_scaler)
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, r2)})
    top_face_index = save_selection(bm)[0]

    # Resize TOP
    r = random.uniform(0.7, 0.9)
    bpy.ops.transform.resize(value=(r, r, r))
    
    # Get TOP location
    bm.faces.ensure_lookup_table()
    top_face = bm.faces[top_face_index]
    face_location = top_face.calc_center_median()
    face_location = activeObject.matrix_world * face_location
    top_z = face_location[2]
    
    # Add little cube
    bpy.ops.mesh.primitive_cube_add(radius=size, location=(x, y, 0))
    bpy.ops.transform.resize(value=(padding/3, padding/3, 1))
    bpy.ops.transform.translate(value = (0, 0, top_z+padding/6))   
    selected_faces = save_selection(bm)

    # Copy it
    for i in range(random.randint(1, 5)):
        bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode": 1}, 
                                    TRANSFORM_OT_translate={"value": (padding*random.uniform(-1.5, 1.5), padding*random.uniform(-1.5, 1.5), 0)})
        bpy.ops.transform.translate(value = (0, 0, random.uniform(-0.2, 0.2)))
    
    # Rotate the cube
    bpy.ops.mesh.select_all(action="SELECT")
    r = radians(random.randrange(3)*90)
    activeObject.rotation_euler = (0,0, r)

    last_index = len(bm.faces)-1
    print(last_index)

    # Add medium cube
    bpy.ops.mesh.primitive_cube_add(radius=size, location=(x, y, 0))
    bpy.ops.transform.resize(value=(1, 0.7, random.uniform(0.5, 3)))
    bm.faces.ensure_lookup_table()
    bpy.ops.mesh.select_all(action="DESELECT")
    bm.faces[last_index+6].select = True
    for i in range(2):
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, 0.05)})
        bpy.ops.transform.resize(value=(1.05, 1.05, 1.05))
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, 0.05)})
        bpy.ops.transform.resize(value=(1/1.05, 1/1.05, 1/1.05))
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, size)})
    for f in bm.faces:
        if f.index > last_index:
            f.select = True    
    bpy.ops.transform.translate(value = (0.1, 0, random.uniform(1, top_z-1)))


    # Bevel first and last mesh
    bpy.ops.mesh.select_all(action="DESELECT")
    bm.faces.ensure_lookup_table()
    bm.faces[last_index+5].select = True
    bm.faces[len(bm.faces)-4].select =True
    bpy.ops.mesh.bevel(offset=0.1)
    
    # Rotate once or not
    r = radians(random.randrange(3)*90)
    activeObject.rotation_euler = (0,0, r)


    
    
    
    # Deselect
    bpy.ops.object.mode_set(mode='OBJECT')

def createParametricalBuilding(x, y, size, pixel):
    print("Building creation")
    
    # Create a cube
    bpy.ops.mesh.primitive_cube_add(radius=size, location=(x, y, 0))    

    # Use a material
    activeObject = bpy.context.active_object
    mat = bpy.data.materials.get("ParamBuilding")
    activeObject.data.materials.append(mat)
    #bpy.context.object.active_material.diffuse_color = [k / 255 for k in pixel]

    # Modifier le cube
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(bpy.context.object.data)
    bm.faces.ensure_lookup_table()
    
    # Define the modifiers
    SUBDIVISION = 9
    
    # Reduce TOP
    bpy.ops.mesh.select_all(action="DESELECT")
    bm.faces[5].select = True
    bpy.ops.transform.translate(value = (0, 0, -size))
    
    top_vert_indexes = []
    first_top_vert_index = 0
    bpy.ops.mesh.select_all(action="DESELECT")
    bpy.ops.mesh.select_mode(type="VERT")
    bm.verts.ensure_lookup_table()
    first_top_vert_index = bm.verts[len(bm.verts)-1].index
    
    # Faire des points
    for i in range(SUBDIVISION+1):
        for j in range(SUBDIVISION+1):
            current_i = i/SUBDIVISION
            current_j = j/SUBDIVISION
            f_i = current_i - 0.5
            f_j = current_j - 0.5
            bpy.ops.mesh.select_all(action="DESELECT")
            bm.verts.ensure_lookup_table()
            bm.verts[first_top_vert_index].select = True
            print(f_i, " | ", f_j)
            bpy.ops.mesh.duplicate_move(TRANSFORM_OT_translate={"value": (-current_i, -current_j, size*3 - pow(f_i+f_j, 2))})
    
    # TOP
    print("SELECT TOP")
    for i in range(SUBDIVISION):
        for j in range(SUBDIVISION):
            print(i, j)
            if j == i-1:
                continue
            bpy.ops.mesh.select_all(action="DESELECT")
            bm.verts.ensure_lookup_table()
            index_1 = (first_top_vert_index+1) + (i*SUBDIVISION) + j
            index_2 = (first_top_vert_index+1) + (i*SUBDIVISION) + j+1
            index_3 = (first_top_vert_index+1) + ((i+1)*SUBDIVISION) + j+1
            index_4 = (first_top_vert_index+1) + ((i+1)*SUBDIVISION) + j+2
            print(index_1, index_2, index_3, index_4)
            bm.verts[index_1].select = True
            bm.verts[index_2].select = True
            bm.verts[index_3].select = True
            bm.verts[index_4].select = True
            bpy.ops.mesh.edge_face_add()
            
            
            
    # UGLY DEBUG for last row
    for i in range(SUBDIVISION-1):
        bpy.ops.mesh.select_all(action="DESELECT")
        bm.verts.ensure_lookup_table()
        i1 = i+(first_top_vert_index+1) + SUBDIVISION*SUBDIVISION
        i2 = i1+1
        i3 = i2+SUBDIVISION
        i4 = i3+1
        bm.verts[i1].select = True
        bm.verts[i2].select = True
        bm.verts[i3].select = True
        bm.verts[i4].select = True
        bpy.ops.mesh.edge_face_add()
            
    bpy.ops.object.mode_set(mode='OBJECT')
    return    
    

    # Sides
    bpy.ops.mesh.select_all(action="DESELECT")
    bm.verts.ensure_lookup_table()
    bm.verts[first_top_vert_index-2].select = True
    for i in range(first_top_vert_index, first_top_vert_index+SUBDIVISION+2):
        print(i)
        bm.verts[i].select = True
    bpy.ops.mesh.edge_face_add()    
            
    bpy.ops.object.mode_set(mode='OBJECT')
    return    
    
    # Run through the pixels
    bpy.ops.object.mode_set(mode='OBJECT')
    return
    for i in range(len(top_vertices_indexes)):
        bm.verts[top_vertices_indexes[i]].select = True
        current_param = abs(i%SUBDIVISION - (SUBDIVISION-1) / 2)/SUBDIVISION
        print(current_param)
        current_translate = pow(current_param, 2)
        bpy.ops.transform.translate(value=(0, 0, current_param))
        bm.verts[top_vertices_indexes[i]].select = False
        if i == 5 :
            break
    
    
    
    
    bpy.ops.object.mode_set(mode='OBJECT')
    return


def save_selection(bm):
    selected_faces = []
    for f in bm.faces:
        if f.select:
            selected_faces.append(f.index)
    return selected_faces
    
# 1 -> 
def use_selection(bm, selected_faces):
    bpy.ops.mesh.select_all(action="DESELECT")
    bm.faces.ensure_lookup_table()
    for i in selected_faces:
        bm.faces[i].select = True
    