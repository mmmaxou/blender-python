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

    # Show the updates in the viewport
    # and recalculate n-gon tessellation.
    bmesh.update_edit_mesh(me, True)
    
    
def showEdgeSelected():
    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    bm.edges.ensure_lookup_table()

    for e in bm.edges:
        if e.select:
            print(e.index)

    # Show the updates in the viewport
    # and recalculate n-gon tessellation.
    bmesh.update_edit_mesh(me, True)
    
def delete_materials():
    for m in bpy.data.materials:
        bpy.data.materials.remove(m)
    
# showFaceSelected()
# showEdgeSelected()
delete_materials()
