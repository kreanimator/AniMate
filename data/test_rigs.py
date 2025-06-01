"""
Test rig configurations for AniMate.
Contains predefined rig setups for testing and development.
"""

from mathutils import Vector

# Basic humanoid test rig configuration
BASIC_HUMANOID = {
    'bones': {
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
    },
    
    'parent_relationships': {
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
}

# Face rig configuration
FACE_RIG = {
    'bones': {
        'jaw': {'head': Vector((0, 0, 0)), 'tail': Vector((0, 0, -0.1))},
        'mouth_left': {'head': Vector((0.1, 0, 0)), 'tail': Vector((0.1, 0, -0.05))},
        'mouth_right': {'head': Vector((-0.1, 0, 0)), 'tail': Vector((-0.1, 0, -0.05))},
        'eyebrow_left': {'head': Vector((0.1, 0, 0.1)), 'tail': Vector((0.1, 0, 0.15))},
        'eyebrow_right': {'head': Vector((-0.1, 0, 0.1)), 'tail': Vector((-0.1, 0, 0.15))}
    },
    
    'parent_relationships': {
        'jaw': ['mouth_left', 'mouth_right'],
        'eyebrow_left': [],
        'eyebrow_right': []
    }
}

# Hand rig configuration
HAND_RIG = {
    'bones': {
        # Thumb
        'thumb_1': {'head': Vector((0, 0, 0)), 'tail': Vector((0.1, 0, 0))},
        'thumb_2': {'head': Vector((0.1, 0, 0)), 'tail': Vector((0.2, 0, 0))},
        'thumb_3': {'head': Vector((0.2, 0, 0)), 'tail': Vector((0.3, 0, 0))},
        
        # Index finger
        'index_1': {'head': Vector((0, 0, 0)), 'tail': Vector((0.1, 0, 0.1))},
        'index_2': {'head': Vector((0.1, 0, 0.1)), 'tail': Vector((0.2, 0, 0.1))},
        'index_3': {'head': Vector((0.2, 0, 0.1)), 'tail': Vector((0.3, 0, 0.1))},
        
        # Middle finger
        'middle_1': {'head': Vector((0, 0, 0)), 'tail': Vector((0.1, 0, 0.2))},
        'middle_2': {'head': Vector((0.1, 0, 0.2)), 'tail': Vector((0.2, 0, 0.2))},
        'middle_3': {'head': Vector((0.2, 0, 0.2)), 'tail': Vector((0.3, 0, 0.2))},
        
        # Ring finger
        'ring_1': {'head': Vector((0, 0, 0)), 'tail': Vector((0.1, 0, 0.3))},
        'ring_2': {'head': Vector((0.1, 0, 0.3)), 'tail': Vector((0.2, 0, 0.3))},
        'ring_3': {'head': Vector((0.2, 0, 0.3)), 'tail': Vector((0.3, 0, 0.3))},
        
        # Pinky
        'pinky_1': {'head': Vector((0, 0, 0)), 'tail': Vector((0.1, 0, 0.4))},
        'pinky_2': {'head': Vector((0.1, 0, 0.4)), 'tail': Vector((0.2, 0, 0.4))},
        'pinky_3': {'head': Vector((0.2, 0, 0.4)), 'tail': Vector((0.3, 0, 0.4))}
    },
    
    'parent_relationships': {
        'thumb_1': ['thumb_2'],
        'thumb_2': ['thumb_3'],
        'index_1': ['index_2'],
        'index_2': ['index_3'],
        'middle_1': ['middle_2'],
        'middle_2': ['middle_3'],
        'ring_1': ['ring_2'],
        'ring_2': ['ring_3'],
        'pinky_1': ['pinky_2'],
        'pinky_2': ['pinky_3']
    }
} 