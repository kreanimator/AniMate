"""
Test rig module for AniMate.
This module provides a simple humanoid rig for testing motion capture functionality.
"""

import bpy
from mathutils import Vector

def create_test_rig():
    """Create a simple humanoid test rig in Blender."""
    # Create armature
    bpy.ops.object.armature_add(enter_editmode=True)
    armature = bpy.context.active_object
    armature.name = "TestRig"
    
    # Clear default bone
    bpy.ops.armature.select_all(action='SELECT')
    bpy.ops.armature.delete()
    
    # Create bones
    bones = {
        'hips': {'head': Vector((0, 0, 0)), 'tail': Vector((0, 0, 0.1))},
        'spine': {'head': Vector((0, 0, 0.1)), 'tail': Vector((0, 0, 0.5))},
        'neck': {'head': Vector((0, 0, 0.5)), 'tail': Vector((0, 0, 0.7))},
        'head': {'head': Vector((0, 0, 0.7)), 'tail': Vector((0, 0, 0.9))},
        
        # Left arm
        'left_shoulder': {'head': Vector((0, 0, 0.5)), 'tail': Vector((0.2, 0, 0.5))},
        'left_upper_arm': {'head': Vector((0.2, 0, 0.5)), 'tail': Vector((0.4, 0, 0.4))},
        'left_lower_arm': {'head': Vector((0.4, 0, 0.4)), 'tail': Vector((0.6, 0, 0.3))},
        'left_hand': {'head': Vector((0.6, 0, 0.3)), 'tail': Vector((0.7, 0, 0.3))},
        
        # Right arm
        'right_shoulder': {'head': Vector((0, 0, 0.5)), 'tail': Vector((-0.2, 0, 0.5))},
        'right_upper_arm': {'head': Vector((-0.2, 0, 0.5)), 'tail': Vector((-0.4, 0, 0.4))},
        'right_lower_arm': {'head': Vector((-0.4, 0, 0.4)), 'tail': Vector((-0.6, 0, 0.3))},
        'right_hand': {'head': Vector((-0.6, 0, 0.3)), 'tail': Vector((-0.7, 0, 0.3))},
        
        # Left leg
        'left_upper_leg': {'head': Vector((0, 0, 0)), 'tail': Vector((0.1, 0, -0.3))},
        'left_lower_leg': {'head': Vector((0.1, 0, -0.3)), 'tail': Vector((0.1, 0, -0.6))},
        'left_foot': {'head': Vector((0.1, 0, -0.6)), 'tail': Vector((0.1, 0.1, -0.7))},
        
        # Right leg
        'right_upper_leg': {'head': Vector((0, 0, 0)), 'tail': Vector((-0.1, 0, -0.3))},
        'right_lower_leg': {'head': Vector((-0.1, 0, -0.3)), 'tail': Vector((-0.1, 0, -0.6))},
        'right_foot': {'head': Vector((-0.1, 0, -0.6)), 'tail': Vector((-0.1, 0.1, -0.7))}
    }
    
    # Create bones
    for bone_name, bone_data in bones.items():
        bpy.ops.armature.bone_primitive_add()
        bone = bpy.context.active_bone
        bone.name = bone_name
        bone.head = bone_data['head']
        bone.tail = bone_data['tail']
    
    # Set up parent relationships
    parent_relationships = {
        'hips': ['spine'],
        'spine': ['neck', 'left_shoulder', 'right_shoulder'],
        'neck': ['head'],
        'left_shoulder': ['left_upper_arm'],
        'left_upper_arm': ['left_lower_arm'],
        'left_lower_arm': ['left_hand'],
        'right_shoulder': ['right_upper_arm'],
        'right_upper_arm': ['right_lower_arm'],
        'right_lower_arm': ['right_hand'],
        'hips': ['left_upper_leg', 'right_upper_leg'],
        'left_upper_leg': ['left_lower_leg'],
        'left_lower_leg': ['left_foot'],
        'right_upper_leg': ['right_lower_leg'],
        'right_lower_leg': ['right_foot']
    }
    
    # Exit edit mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return armature

def setup_test_scene():
    """Set up a test scene with camera and lighting."""
    # Create camera
    bpy.ops.object.camera_add(location=(0, -5, 2), rotation=(1.0, 0, 0))
    camera = bpy.context.active_object
    bpy.context.scene.camera = camera
    
    # Create light
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 5))
    
    # Set render settings
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'GPU'
    
    return camera

if __name__ == "__main__":
    # Create test rig and scene
    rig = create_test_rig()
    camera = setup_test_scene()
    
    print("Test rig created successfully!") 