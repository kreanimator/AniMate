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
            # Right hand fingers only
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
            # Left hand fingers only
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
            **{f'mixamorig:RightHandThumb{i}': lambda e: Euler((e.x, e.y, e.z)) for i in range(1, 4)},
            **{f'mixamorig:RightHandIndex{i}': lambda e: Euler((e.x, e.y, e.z)) for i in range(1, 4)},
            **{f'mixamorig:RightHandMiddle{i}': lambda e: Euler((e.x, e.y, e.z)) for i in range(1, 4)},
            **{f'mixamorig:RightHandRing{i}': lambda e: Euler((e.x, e.y, e.z)) for i in range(1, 4)},
            **{f'mixamorig:RightHandPinky{i}': lambda e: Euler((e.x, e.y, e.z)) for i in range(1, 4)},
            **{f'mixamorig:LeftHandThumb{i}': lambda e: Euler((e.x, e.y, e.z)) for i in range(1, 4)},
            **{f'mixamorig:LeftHandIndex{i}': lambda e: Euler((e.x, e.y, e.z)) for i in range(1, 4)},
            **{f'mixamorig:LeftHandMiddle{i}': lambda e: Euler((e.x, e.y, e.z)) for i in range(1, 4)},
            **{f'mixamorig:LeftHandRing{i}': lambda e: Euler((e.x, e.y, e.z)) for i in range(1, 4)},
            **{f'mixamorig:LeftHandPinky{i}': lambda e: Euler((e.x, e.y, e.z)) for i in range(1, 4)},
        }

    def get_hand_remap_table(self):
        """
        Returns remap tables for all hand joints (both hands).
        Each entry is a tuple: (input_range, output_range)
        """
        return {
            # Right hand
            "RightHandThumb1":  ((0.011, 0.630), (-.60, 0.63)),
            "RightHandThumb2":  ((0.010, 0.536), (-.30, 0.54)),
            "RightHandThumb3":  ((0.008, 1.035), (-.15, 1.03)),
            "RightHandIndex1":  ((0.105, 1.331), (-.50, 1.33)),
            "RightHandIndex2":  ((0.014, 1.858), (-.20, 1.86)),
            "RightHandIndex3":  ((0.340, 1.523), (-.55, 1.52)),
            "RightHandMiddle1": ((0.046, 1.326), (-.50, 1.33)),
            "RightHandMiddle2": ((0.330, 1.803), (-.30, 1.80)),
            "RightHandMiddle3": ((0.007, 1.911), (-.15, 1.91)),
            "RightHandRing1":   ((0.012, 1.477), (-.60, 1.48)),
            "RightHandRing2":   ((0.244, 1.674), (-.30, 1.67)),
            "RightHandRing3":   ((0.021, 1.614), (-.30, 1.61)),
            "RightHandPinky1":  ((0.120, 1.322), (-.80, 1.32)),
            "RightHandPinky2":  ((0.213, 1.584), (-.50, 1.58)),
            "RightHandPinky3":  ((0.018, 1.937), (-.30, 1.94)),
            # Left hand
            "LeftHandThumb1":  ((0.011, 0.630), (-.60, 0.63)),
            "LeftHandThumb2":  ((0.010, 0.536), (-.30, 0.54)),
            "LeftHandThumb3":  ((0.008, 1.035), (-.15, 1.03)),
            "LeftHandIndex1":  ((0.105, 1.331), (-.50, 1.33)),
            "LeftHandIndex2":  ((0.014, 1.858), (-.20, 1.86)),
            "LeftHandIndex3":  ((0.340, 1.523), (-.55, 1.52)),
            "LeftHandMiddle1": ((0.046, 1.326), (-.50, 1.33)),
            "LeftHandMiddle2": ((0.330, 1.803), (-.30, 1.80)),
            "LeftHandMiddle3": ((0.007, 1.911), (-.15, 1.91)),
            "LeftHandRing1":   ((0.012, 1.477), (-.60, 1.48)),
            "LeftHandRing2":   ((0.244, 1.674), (-.30, 1.67)),
            "LeftHandRing3":   ((0.021, 1.614), (-.30, 1.61)),
            "LeftHandPinky1":  ((0.120, 1.322), (-.80, 1.32)),
            "LeftHandPinky2":  ((0.213, 1.584), (-.50, 1.58)),
            "LeftHandPinky3":  ((0.018, 1.937), (-.30, 1.94)),
        } 
        