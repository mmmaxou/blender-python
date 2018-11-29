import bpy
import bmesh
import random
import ut

print(">> Running Script")

def get_random_color():
    ''' generate rgb using a list comprehension '''
    r, g, b = [random.random() for i in range(3)]
    return (r, g, b, 1)
  
# Clear Scene
if bpy.context.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')
# print(tuple(bpy.context.scene.tool_settings.mesh_select_mode))
if bpy.context.scene.tool_settings.mesh_select_mode != (False, False, True):
    bpy.context.scene.tool_settings.mesh_select_mode = (False, False, True)
ut.delete_all()

# Create loop of cubes
countX = random.randrange(10, 20)
countY = random.randrange(10, 20)
size = 0.5
padding = 0.2


for i in range(0, countX):
    for j in range(0, countY):
        x = i*2*(padding+size) - (countX+padding*countX)/2
        y = j*2*(padding+size) - (countY+padding*countY)/2
        obj = bpy.ops.mesh.primitive_cube_add(radius=size, location=(x, y, 0))
        color = list(np.random.choice(range(256), size=3))
        obj.color = color  
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action="DESELECT")
        bm = bmesh.from_edit_mesh(bpy.context.object.data)
        bm.faces.ensure_lookup_table()
        bm.faces[5].select = True
        bpy.ops.transform.translate(value = (0, 0, random.randrange(2, 10)))
        bpy.ops.object.mode_set(mode='OBJECT')
