"""
Mixamo rig mapping implementation.
"""
from .base_mappings import BaseRigMapping

class MixamoMapping(BaseRigMapping):
    """Mapping implementation for Mixamo rigs."""
    
    def get_pose_mapping(self):
        return {
            # Spine
            'Spine': [11, 23],  # Shoulder to Hip
            'Spine1': [23, 24],  # Hip to Hip
            'Spine2': [24, 12],  # Hip to Shoulder
            
            # Head
            'Neck': [11, 0],  # Shoulder to Nose
            'Head': [0, 8],  # Nose to Forehead
            
            # Left Arm
            'LeftShoulder': [11, 13],  # Shoulder to Elbow
            'LeftArm': [13, 15],  # Elbow to Wrist
            
            # Right Arm
            'RightShoulder': [12, 14],  # Shoulder to Elbow
            'RightArm': [14, 16],  # Elbow to Wrist
            
            # Left Leg
            'LeftUpLeg': [23, 25],  # Hip to Knee
            'LeftLeg': [25, 27],  # Knee to Ankle
            'LeftFoot': [27, 31],  # Ankle to Heel
            
            # Right Leg
            'RightUpLeg': [24, 26],  # Hip to Knee
            'RightLeg': [26, 28],  # Knee to Ankle
            'RightFoot': [28, 32],  # Ankle to Heel
        }
    
    def get_hand_mapping(self):
        return {
            # Thumb
            'Thumb1': [0, 1],
            'Thumb2': [1, 2],
            'Thumb3': [2, 3],
            
            # Index
            'Index1': [0, 5],
            'Index2': [5, 6],
            'Index3': [6, 7],
            
            # Middle
            'Middle1': [0, 9],
            'Middle2': [9, 10],
            'Middle3': [10, 11],
            
            # Ring
            'Ring1': [0, 13],
            'Ring2': [13, 14],
            'Ring3': [14, 15],
            
            # Pinky
            'Pinky1': [0, 17],
            'Pinky2': [17, 18],
            'Pinky3': [18, 19]
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