import bpy
import os
import ut
import sys
import flat
import importlib
from time import sleep

blend_dir = os.path.dirname(bpy.data.filepath)
if blend_dir not in sys.path:
   sys.path.append(blend_dir)

importlib.reload(flat)

dir_path = os.path.dirname(os.path.realpath(__file__)).replace("Scripting.blend", "")
# file=open(dir_path + "map-simple.ppm", "r")
file=open(dir_path + "map.ppm", "r")

# Read ppm
lines=file.readlines()
version=lines[0]
comments=lines[1]
size = [int(i) for i in lines[2].split()]
width = size[0]
height = size[1]
max_color_value=lines[3]
# print("Comments: ", comments)
# print("Size: ", size)
# print("Version: ", version)
# print("max color values: ", max_color_value)
pixels = [[0 for i in range(height)] for j in range(width)]
for i in range(0, width):
    for j in range(0, height):
        index=((i*height)+j)*3+4
        pixel = [int(lines[index]), int(lines[index+1]), int(lines[index+2])]
        pixels[i][j] = pixel

# Analyse it
def isWhite(pixel):
    return (pixel[0]==255 and pixel[1]==255 and pixel[2]==255)

def isBlack(pixel):
    return (pixel[0]==0 and pixel[1]==0 and pixel[2]==0)

def isRed(pixel):
    return (pixel[0]==255 and pixel[1]==0 and pixel[2]==0)

def isGreen(pixel):
    return (pixel[0]==0 and pixel[1]==255 and pixel[2]==0)

def createSimpleCube(x, y, i, j, size, pixel):
    # Create a cube
    bpy.ops.mesh.primitive_cube_add(radius=size, location=(x, y, 0))
    activeObject = bpy.context.active_object
    mat = bpy.data.materials.new(name="MaterialName")
    activeObject.data.materials.append(mat)
    bpy.context.object.active_material.diffuse_color = [k / 255 for k in pixel]

# Clear Scene


print("===SCRIPT STARTING===")
if bpy.context.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')
# print(tuple(bpy.context.scene.tool_settings.mesh_select_mode))
if bpy.context.scene.tool_settings.mesh_select_mode != (False, False, True):
    bpy.context.scene.tool_settings.mesh_select_mode = (False, False, True)
# Delete all material
for m in bpy.data.materials:
    bpy.data.materials.remove(m)
ut.delete_all()


# Display
padding = 0.1
size = 0.5
total_size_x = width*(padding+size)
total_size_y = height*(padding+size)
for i in range(0, width):
    for j in range(0, height):
        if not isWhite(pixels[i][j]): 
            x = i*2*(padding+size) - (width+padding*width)/2
            y = j*2*(padding+size) - (height+padding*height)/2
            # print("[", i, "][", j,"]: ", img[i][j])
            x -= (total_size_x/2)
            y -= (total_size_y/2)

            if isGreen(pixels[i][j]):
                createSimpleCube(x, y, i, j, size, pixels[i][j])

            if isRed(pixels[i][j]):
                # flat.createFlat(x, y, size, pixels[i][j])
                flat.createBuilding(x, y, size, pixels[i][j])

        if isBlack(pixels[i][j]): 
            print("> Black")
