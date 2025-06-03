"""
Mixamo rig mapping implementation.
"""
from .base_mappings import BaseRigMapping
from mathutils import Euler

class MixamoMapping(BaseRigMapping):
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
        return {
            "Hips": [23, 24],
            "Spine": [23, 11],
            "Spine1": [11, 12],
            "Spine2": [12, 0],
            "Neck": [0, 2],
            "Head": [2, 8],
            "RightShoulder": [11, 12],
            "RightArm": [12, 14],
            "RightForeArm": [14, 16],
            "LeftShoulder": [11, 12],
            "LeftArm": [12, 13],
            "LeftForeArm": [13, 15],
        }

    def get_face_mapping(self):
        return {
            "Head": [0, 1],
            "Neck": [1, 2],
        }

    def get_hand_mapping(self):
        return {
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
        from mathutils import Euler
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
        