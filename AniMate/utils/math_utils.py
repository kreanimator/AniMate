import math
from mathutils import Vector, Matrix

ROT_YUP_TO_ZUP = Matrix.Rotation(-math.pi / 2, 4, 'X')

def mediapipe_to_blender_coords(landmark, image_width, image_height, flip_x=True):
    x = landmark.x * image_width
    y = landmark.y * image_height
    z = landmark.z * image_width
    if flip_x:
        x = image_width - x
    vec = Vector((x, y, z))
    vec = ROT_YUP_TO_ZUP @ vec
    return vec

def mediapipe_to_blender_coords_pose(landmark, image_width, image_height, flip_x=True):
    x = landmark.x * image_width
    y = landmark.y * image_height
    z = landmark.z * image_width
    if flip_x:
        x = image_width - x
    vec = Vector((x, y, z))
    vec = ROT_YUP_TO_ZUP @ vec
    return vec

def remap(val, in_min, in_max, out_min, out_max):
    val = max(min(val, in_max), in_min)
    return out_min + (float(val - in_min) / float(in_max - in_min)) * (out_max - out_min) 
    