"""
Bone mapping configurations for AniMate.
Contains mappings between MediaPipe landmarks and Blender bones.
"""

# MediaPipe pose landmarks to Blender bone mapping
POSE_LANDMARKS_TO_BONES = {
    # Torso
    'hips': [23, 24],           # Left and right hip
    'spine': [11, 12],          # Left and right shoulder
    'neck': [11, 12],           # Shoulders midpoint to head
    'head': [0],                # Nose
    
    # Arms
    'left_shoulder': [11],
    'left_upper_arm': [11, 13],
    'left_lower_arm': [13, 15],
    'left_hand': [15, 17],
    
    'right_shoulder': [12],
    'right_upper_arm': [12, 14],
    'right_lower_arm': [14, 16],
    'right_hand': [16, 18],
    
    # Legs
    'left_upper_leg': [23, 25],
    'left_lower_leg': [25, 27],
    'left_foot': [27, 31],
    
    'right_upper_leg': [24, 26],
    'right_lower_leg': [26, 28],
    'right_foot': [28, 32]
}

# MediaPipe face landmarks to Blender shape keys/bones
FACE_LANDMARKS_TO_BONES = {
    'jaw': [0, 17, 57, 287],  # Jaw opening
    'mouth_left': [61, 291],   # Mouth corner L
    'mouth_right': [291, 61],  # Mouth corner R
    'eyebrow_left': [70, 63, 105, 66, 107],  # Left eyebrow
    'eyebrow_right': [336, 296, 334, 293, 300]  # Right eyebrow
}

# MediaPipe hand landmarks to Blender finger bones
HAND_LANDMARKS_TO_BONES = {
    'thumb': [1, 2, 3, 4],
    'index': [5, 6, 7, 8],
    'middle': [9, 10, 11, 12],
    'ring': [13, 14, 15, 16],
    'pinky': [17, 18, 19, 20]
} 