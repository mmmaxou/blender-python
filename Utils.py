import bpy
import bmesh

def showFaceSelected():
    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    bm.faces.ensure_lookup_table()

    for f in bm.faces:
        if f.select:
            print(f.index)    
    
def showEdgeSelected():
    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    bm.edges.ensure_lookup_table()

    for e in bm.edges:
        if e.select:
            print(e.index)
    
def showVertSelected():
    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    bm.verts.ensure_lookup_table()

    for v in bm.verts:
        if v.select:
            print(v.index)
    
def delete_materials():
    for m in bpy.data.materials:
        bpy.data.materials.remove(m)
    
print("__ UTILS __")
showFaceSelected()
# showEdgeSelected()
# showVertSelected()
# delete_materials()
