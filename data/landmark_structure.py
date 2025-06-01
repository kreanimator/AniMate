"""
MediaPipe landmark structure definitions.
This module contains the mapping of MediaPipe landmarks to their corresponding indices and descriptions.
"""

# MediaPipe Pose landmarks
POSE_LANDMARKS = {
    # Face landmarks
    "nose": 0,
    "left_eye_inner": 1,
    "left_eye": 2,
    "left_eye_outer": 3,
    "right_eye_inner": 4,
    "right_eye": 5,
    "right_eye_outer": 6,
    "left_ear": 7,
    "right_ear": 8,
    "mouth_left": 9,
    "mouth_right": 10,
    
    # Upper body
    "left_shoulder": 11,
    "right_shoulder": 12,
    "left_elbow": 13,
    "right_elbow": 14,
    "left_wrist": 15,
    "right_wrist": 16,
    "left_pinky": 17,
    "right_pinky": 18,
    "left_index": 19,
    "right_index": 20,
    "left_thumb": 21,
    "right_thumb": 22,
    
    # Lower body
    "left_hip": 23,
    "right_hip": 24,
    "left_knee": 25,
    "right_knee": 26,
    "left_ankle": 27,
    "right_ankle": 28,
    "left_heel": 29,
    "right_heel": 30,
    "left_foot_index": 31,
    "right_foot_index": 32
}

# MediaPipe Face Mesh landmarks (key points)
FACE_LANDMARKS = {
    # Jaw
    "jaw_left": 234,
    "jaw_right": 454,
    "jaw_center": 152,
    
    # Mouth
    "mouth_left": 61,
    "mouth_right": 291,
    "mouth_top": 13,
    "mouth_bottom": 14,
    
    # Eyes
    "left_eye_outer": 33,
    "left_eye_inner": 133,
    "left_eye_top": 159,
    "left_eye_bottom": 145,
    "right_eye_outer": 263,
    "right_eye_inner": 362,
    "right_eye_top": 386,
    "right_eye_bottom": 374,
    
    # Eyebrows
    "left_eyebrow_outer": 70,
    "left_eyebrow_inner": 105,
    "right_eyebrow_outer": 300,
    "right_eyebrow_inner": 334
}

# MediaPipe Hand landmarks
HAND_LANDMARKS = {
    # Wrist
    "wrist": 0,
    
    # Thumb
    "thumb_cmc": 1,
    "thumb_mcp": 2,
    "thumb_ip": 3,
    "thumb_tip": 4,
    
    # Index finger
    "index_finger_mcp": 5,
    "index_finger_pip": 6,
    "index_finger_dip": 7,
    "index_finger_tip": 8,
    
    # Middle finger
    "middle_finger_mcp": 9,
    "middle_finger_pip": 10,
    "middle_finger_dip": 11,
    "middle_finger_tip": 12,
    
    # Ring finger
    "ring_finger_mcp": 13,
    "ring_finger_pip": 14,
    "ring_finger_dip": 15,
    "ring_finger_tip": 16,
    
    # Pinky
    "pinky_mcp": 17,
    "pinky_pip": 18,
    "pinky_dip": 19,
    "pinky_tip": 20
}

# Landmark connections for visualization
LANDMARK_CONNECTIONS = {
    "pose": [
        # Face
        (0, 1), (1, 2), (2, 3),  # Left eye
        (0, 4), (4, 5), (5, 6),  # Right eye
        (0, 7), (0, 8),  # Ears
        (9, 10),  # Mouth
        
        # Upper body
        (11, 12),  # Shoulders
        (11, 13), (13, 15),  # Left arm
        (12, 14), (14, 16),  # Right arm
        
        # Lower body
        (23, 24),  # Hips
        (23, 25), (25, 27),  # Left leg
        (24, 26), (26, 28),  # Right leg
    ],
    
    "face": [
        # Jaw
        (234, 152), (152, 454),
        
        # Mouth
        (61, 13), (13, 291), (291, 14), (14, 61),
        
        # Left eye
        (33, 133), (133, 159), (159, 145), (145, 33),
        
        # Right eye
        (263, 362), (362, 386), (386, 374), (374, 263),
        
        # Eyebrows
        (70, 105), (300, 334)
    ],
    
    "hand": [
        # Thumb
        (0, 1), (1, 2), (2, 3), (3, 4),
        
        # Index finger
        (0, 5), (5, 6), (6, 7), (7, 8),
        
        # Middle finger
        (0, 9), (9, 10), (10, 11), (11, 12),
        
        # Ring finger
        (0, 13), (13, 14), (14, 15), (15, 16),
        
        # Pinky
        (0, 17), (17, 18), (18, 19), (19, 20)
    ]
}
