"""
Mixamo rig mapping implementation.
"""
from .base_mappings import BaseRigMapping

class MixamoMapping(BaseRigMapping):
    """Mapping implementation for Mixamo rigs."""
    
    def get_pose_mapping(self):
        # MediaPipe Pose indices: https://google.github.io/mediapipe/solutions/pose.html#pose-landmark-model-blazepose-ghum-3d
        return {
            # Hips and Spine
            'Hips': [23, 24],  # left_hip to right_hip
            'Spine': [23, 11],  # left_hip to left_shoulder
            'Spine1': [11, 12],  # left_shoulder to right_shoulder
            'Spine2': [12, 0],  # right_shoulder to nose (approximate upper spine)
            'Neck': [0, 1],  # nose to left_eye_inner (approximate neck)
            'Head': [0, 8],  # nose to forehead (approximate)
            'HeadTop_End': [8, 8],  # forehead (no landmark for head top, so repeat)

            # Right Arm
            'RightShoulder': [12, 14],  # right_shoulder to right_elbow
            'RightArm': [14, 16],  # right_elbow to right_wrist
            'RightForeArm': [14, 16],  # same as above (no separate landmark)
            'RightHand': [16, 16],  # right_wrist (single point)

            # Left Arm
            'LeftShoulder': [11, 13],  # left_shoulder to left_elbow
            'LeftArm': [13, 15],  # left_elbow to left_wrist
            'LeftForeArm': [13, 15],  # same as above
            'LeftHand': [15, 15],  # left_wrist

            # Right Leg
            'RightUpLeg': [24, 26],  # right_hip to right_knee
            'RightLeg': [26, 28],  # right_knee to right_ankle
            'RightFoot': [28, 32],  # right_ankle to right_heel
            'RightToeBase': [32, 32],  # right_heel (no separate toe landmark)
            'RightToe_End': [32, 32],  # right_heel (repeat, or remove if not needed)

            # Left Leg
            'LeftUpLeg': [23, 25],  # left_hip to left_knee
            'LeftLeg': [25, 27],  # left_knee to left_ankle
            'LeftFoot': [27, 31],  # left_ankle to left_heel
            'LeftToeBase': [31, 31],  # left_heel
            'LeftToe_End': [31, 31],  # left_heel
        }
    
    def get_hand_mapping(self):
        # MediaPipe Hands indices: https://google.github.io/mediapipe/solutions/hands.html#hand-landmark-model
        # Thumb: 1-2-3-4, Index: 5-6-7-8, Middle: 9-10-11-12, Ring: 13-14-15-16, Pinky: 17-18-19-20
        # Wrist: 0
        return {
            # Right hand (use same for left, code will swap as needed)
            'RightHand': [0, 0],  # wrist
            'RightHandThumb1': [1, 2],
            'RightHandThumb2': [2, 3],
            'RightHandThumb3': [3, 4],
            'RightHandIndex1': [5, 6],
            'RightHandIndex2': [6, 7],
            'RightHandIndex3': [7, 8],
            'RightHandMiddle1': [9, 10],
            'RightHandMiddle2': [10, 11],
            'RightHandMiddle3': [11, 12],
            'RightHandRing1': [13, 14],
            'RightHandRing2': [14, 15],
            'RightHandRing3': [15, 16],
            'RightHandPinky1': [17, 18],
            'RightHandPinky2': [18, 19],
            'RightHandPinky3': [19, 20],
            # Left hand (same indices, code will handle side)
            'LeftHand': [0, 0],
            'LeftHandThumb1': [1, 2],
            'LeftHandThumb2': [2, 3],
            'LeftHandThumb3': [3, 4],
            'LeftHandIndex1': [5, 6],
            'LeftHandIndex2': [6, 7],
            'LeftHandIndex3': [7, 8],
            'LeftHandMiddle1': [9, 10],
            'LeftHandMiddle2': [10, 11],
            'LeftHandMiddle3': [11, 12],
            'LeftHandRing1': [13, 14],
            'LeftHandRing2': [14, 15],
            'LeftHandRing3': [15, 16],
            'LeftHandPinky1': [17, 18],
            'LeftHandPinky2': [18, 19],
            'LeftHandPinky3': [19, 20],
        }
    
    def get_face_mapping(self):
        return {
            'Jaw': [152, 175],  # Jaw movement
            'LeftEye': [33, 133],  # Left eye movement
            'RightEye': [362, 263],  # Right eye movement
        }
    
    def get_bone_hierarchy(self):
        return {
            "Hips": {
                "Spine": {
                    "Spine1": {
                        "Spine2": {
                            "Neck": {
                                "Head": {
                                    "HeadTop_End": {}
                                }
                            }
                        }
                    }
                },
                "LeftUpLeg": {
                    "LeftLeg": {
                        "LeftFoot": {
                            "LeftToeBase": {
                                "LeftToe_End": {}
                            }
                        }
                    }
                },
                "RightUpLeg": {
                    "RightLeg": {
                        "RightFoot": {
                            "RightToeBase": {
                                "RightToe_End": {}
                            }
                        }
                    }
                },
                "LeftShoulder": {
                    "LeftArm": {
                        "LeftForeArm": {
                            "LeftHand": {
                                "LeftHandThumb1": {
                                    "LeftHandThumb2": {
                                        "LeftHandThumb3": {}
                                    }
                                },
                                "LeftHandIndex1": {
                                    "LeftHandIndex2": {
                                        "LeftHandIndex3": {}
                                    }
                                },
                                "LeftHandMiddle1": {
                                    "LeftHandMiddle2": {
                                        "LeftHandMiddle3": {}
                                    }
                                },
                                "LeftHandRing1": {
                                    "LeftHandRing2": {
                                        "LeftHandRing3": {}
                                    }
                                },
                                "LeftHandPinky1": {
                                    "LeftHandPinky2": {
                                        "LeftHandPinky3": {}
                                    }
                                }
                            }
                        }
                    }
                },
                "RightShoulder": {
                    "RightArm": {
                        "RightForeArm": {
                            "RightHand": {
                                "RightHandThumb1": {
                                    "RightHandThumb2": {
                                        "RightHandThumb3": {}
                                    }
                                },
                                "RightHandIndex1": {
                                    "RightHandIndex2": {
                                        "RightHandIndex3": {}
                                    }
                                },
                                "RightHandMiddle1": {
                                    "RightHandMiddle2": {
                                        "RightHandMiddle3": {}
                                    }
                                },
                                "RightHandRing1": {
                                    "RightHandRing2": {
                                        "RightHandRing3": {}
                                    }
                                },
                                "RightHandPinky1": {
                                    "RightHandPinky2": {
                                        "RightHandPinky3": {}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    
    def get_bone_rotation_limits(self):
        """Get the rotation limits for each bone in degrees."""
        return {
            'Spine': {'x': (-30, 30), 'y': (-30, 30), 'z': (-30, 30)},
            'Neck': {'x': (-30, 30), 'y': (-30, 30), 'z': (-30, 30)},
            'LeftShoulder': {'x': (-90, 90), 'y': (-90, 90), 'z': (-90, 90)},
            'RightShoulder': {'x': (-90, 90), 'y': (-90, 90), 'z': (-90, 90)},
            # Add more bone limits as needed
        }
    
    def get_bone_scale_factors(self):
        """Get the scale factors for each bone."""
        return {
            'Spine': 1.0,
            'Neck': 1.0,
            'LeftShoulder': 1.0,
            'RightShoulder': 1.0,
            # Add more bone scale factors as needed
        }

    def get_capabilities(self):
        return {
            'face': False,
            'hands': True,
        } 