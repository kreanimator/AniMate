"""
Mixamo rig mapping implementation.
"""
from .base_mappings import BaseRigMapping
from mathutils import Vector, Matrix, Euler



class MixamoMapping(BaseRigMapping):
    """Mapping for Mixamo rigs."""

    def get_bone_hierarchy(self):
        """Get the expected bone hierarchy for Mixamo rigs."""
        return {
            "Hips": {
                "Spine": {
                    "Spine1": {
                        "Spine2": {
                            "Neck": {
                                "Head": {
                                    "HeadTop_End": {}
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
                            }
                        }
                    }
                }
            }
        }

    def get_pose_mapping(self):
        """Get the mapping between MediaPipe pose landmarks and bone names."""
        return {
            "Hips": [23, 24],  # Left and right hip
            "Spine": [23, 11],  # Hip to mid-spine
            "Spine1": [11, 12],  # Mid-spine to upper spine
            "Spine2": [12, 0],  # Upper spine to neck
            "Neck": [0, 2],  # Neck to head
            "Head": [2, 8],  # Head to nose
            "RightShoulder": [11, 12],  # Spine to right shoulder
            "RightArm": [12, 14],  # Shoulder to elbow
            "RightForeArm": [14, 16],  # Elbow to wrist
            "LeftShoulder": [11, 12],  # Spine to left shoulder
            "LeftArm": [12, 13],  # Shoulder to elbow
            "LeftForeArm": [13, 15],  # Elbow to wrist
        }

    def get_face_mapping(self):
        """Get the mapping between MediaPipe face landmarks and bone names."""
        return {
            "Head": [0, 1],  # Nose to forehead
            "Neck": [1, 2],  # Forehead to chin
        }

    def get_hand_mapping(self):
        """Get the mapping between MediaPipe hand landmarks and bone names."""
        return {
            # Right hand
            "RightHandThumb1": [0, 1],
            "RightHandThumb2": [1, 2],
            "RightHandThumb3": [2, 3],
            "RightHandIndex1": [0, 5],
            "RightHandIndex2": [5, 6],
            "RightHandIndex3": [6, 7],
            "RightHandMiddle1": [0, 9],
            "RightHandMiddle2": [9, 10],
            "RightHandMiddle3": [10, 11],
            "RightHandRing1": [0, 13],
            "RightHandRing2": [13, 14],
            "RightHandRing3": [14, 15],
            "RightHandPinky1": [0, 17],
            "RightHandPinky2": [17, 18],
            "RightHandPinky3": [18, 19],
            # Left hand
            "LeftHandThumb1": [0, 1],
            "LeftHandThumb2": [1, 2],
            "LeftHandThumb3": [2, 3],
            "LeftHandIndex1": [0, 5],
            "LeftHandIndex2": [5, 6],
            "LeftHandIndex3": [6, 7],
            "LeftHandMiddle1": [0, 9],
            "LeftHandMiddle2": [9, 10],
            "LeftHandMiddle3": [10, 11],
            "LeftHandRing1": [0, 13],
            "LeftHandRing2": [13, 14],
            "LeftHandRing3": [14, 15],
            "LeftHandPinky1": [0, 17],
            "LeftHandPinky2": [17, 18],
            "LeftHandPinky3": [18, 19],
        }

    def get_bone_rotation_limits(self):
        """Get rotation limits for each bone."""
        return {
            "Hips": {"x": (-45, 45), "y": (-45, 45), "z": (-45, 45)},
            "Spine": {"x": (-30, 30), "y": (-30, 30), "z": (-30, 30)},
            "Spine1": {"x": (-30, 30), "y": (-30, 30), "z": (-30, 30)},
            "Spine2": {"x": (-30, 30), "y": (-30, 30), "z": (-30, 30)},
            "Neck": {"x": (-45, 45), "y": (-45, 45), "z": (-45, 45)},
            "Head": {"x": (-45, 45), "y": (-45, 45), "z": (-45, 45)},
            "RightShoulder": {"x": (-90, 90), "y": (-90, 90), "z": (-90, 90)},
            "RightArm": {"x": (-90, 90), "y": (-90, 90), "z": (-90, 90)},
            "RightForeArm": {"x": (-90, 90), "y": (-90, 90), "z": (-90, 90)},
            "LeftShoulder": {"x": (-90, 90), "y": (-90, 90), "z": (-90, 90)},
            "LeftArm": {"x": (-90, 90), "y": (-90, 90), "z": (-90, 90)},
            "LeftForeArm": {"x": (-90, 90), "y": (-90, 90), "z": (-90, 90)},
        }

    def get_bone_scale_factors(self):
        """Get scale factors for each bone's rotation."""
        return {
            "Hips": 1.0,
            "Spine": 1.0,
            "Spine1": 1.0,
            "Spine2": 1.0,
            "Neck": 1.0,
            "Head": 1.0,
            "RightShoulder": 1.0,
            "RightArm": 1.0,
            "RightForeArm": 1.0,
            "LeftShoulder": 1.0,
            "LeftArm": 1.0,
            "LeftForeArm": 1.0,
        }

    def get_capabilities(self):
        return {
            'face': False,
            'hands': True,
        }

    def get_axis_corrections(self):
        return {
            # Torso
            'mixamorig:Hips': lambda e: Euler((e.x, e.y, e.z)),
            'mixamorig:Spine': lambda e: Euler((e.x, e.y, e.z)),
            'mixamorig:Spine1': lambda e: Euler((e.x, e.y, e.z)),
            'mixamorig:Spine2': lambda e: Euler((e.x, e.y, e.z)),
            'mixamorig:Neck': lambda e: Euler((e.x, e.y, e.z)),
            'mixamorig:Head': lambda e: Euler((e.x, e.y, e.z)),
            'mixamorig:HeadTop_End': lambda e: Euler((e.x, e.y, e.z)),
            # Shoulders
            'mixamorig:RightShoulder': lambda e: Euler((e.x, e.y, e.z)),
            'mixamorig:LeftShoulder': lambda e: Euler((e.x, e.y, e.z)),
            # Arms (swap/invert Y as a starting point)
            'mixamorig:RightArm': lambda e: Euler((e.x, -e.y, e.z)),
            'mixamorig:RightForeArm': lambda e: Euler((e.x, -e.y, e.z)),
            'mixamorig:RightHand': lambda e: Euler((e.x, -e.y, e.z)),
            'mixamorig:LeftArm': lambda e: Euler((e.x, -e.y, e.z)),
            'mixamorig:LeftForeArm': lambda e: Euler((e.x, -e.y, e.z)),
            'mixamorig:LeftHand': lambda e: Euler((e.x, -e.y, e.z)),
            # Fingers (identity, tune as needed)
            **{f'mixamorig:RightHandThumb{i}': lambda e: Euler((e.x, e.y, e.z)) for i in range(1, 5)},
            **{f'mixamorig:RightHandIndex{i}': lambda e: Euler((e.x, e.y, e.z)) for i in range(1, 5)},
            **{f'mixamorig:RightHandMiddle{i}': lambda e: Euler((e.x, e.y, e.z)) for i in range(1, 5)},
            **{f'mixamorig:RightHandRing{i}': lambda e: Euler((e.x, e.y, e.z)) for i in range(1, 5)},
            **{f'mixamorig:RightHandPinky{i}': lambda e: Euler((e.x, e.y, e.z)) for i in range(1, 5)},
            **{f'mixamorig:LeftHandThumb{i}': lambda e: Euler((e.x, e.y, e.z)) for i in range(1, 5)},
            **{f'mixamorig:LeftHandIndex{i}': lambda e: Euler((e.x, e.y, e.z)) for i in range(1, 5)},
            **{f'mixamorig:LeftHandMiddle{i}': lambda e: Euler((e.x, e.y, e.z)) for i in range(1, 5)},
            **{f'mixamorig:LeftHandRing{i}': lambda e: Euler((e.x, e.y, e.z)) for i in range(1, 5)},
            **{f'mixamorig:LeftHandPinky{i}': lambda e: Euler((e.x, e.y, e.z)) for i in range(1, 5)},
            # Legs (swap/invert Y as a starting point)
            'mixamorig:RightUpLeg': lambda e: Euler((e.x, -e.y, e.z)),
            'mixamorig:RightLeg': lambda e: Euler((e.x, -e.y, e.z)),
            'mixamorig:RightFoot': lambda e: Euler((e.x, -e.y, e.z)),
            'mixamorig:RightToeBase': lambda e: Euler((e.x, -e.y, e.z)),
            'mixamorig:RightToe_End': lambda e: Euler((e.x, -e.y, e.z)),
            'mixamorig:LeftUpLeg': lambda e: Euler((e.x, -e.y, e.z)),
            'mixamorig:LeftLeg': lambda e: Euler((e.x, -e.y, e.z)),
            'mixamorig:LeftFoot': lambda e: Euler((e.x, -e.y, e.z)),
            'mixamorig:LeftToeBase': lambda e: Euler((e.x, -e.y, e.z)),
            'mixamorig:LeftToe_End': lambda e: Euler((e.x, -e.y, e.z)),
        }
