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
        # MediaPipe hand indices: https://google.github.io/mediapipe/solutions/hands.html#hand-landmark-model
        # Thumb: CMC(1), MCP(2), IP(3), TIP(4)
        # Index: MCP(5), PIP(6), DIP(7), TIP(8)
        # Middle: MCP(9), PIP(10), DIP(11), TIP(12)
        # Ring: MCP(13), PIP(14), DIP(15), TIP(16)
        # Pinky: MCP(17), PIP(18), DIP(19), TIP(20)
        return {
            # Right hand fingers (use 3 indices for angle: base, mid, tip)
            "RightHandThumb1": [1, 2, 3],
            "RightHandThumb2": [2, 3, 4],
            "RightHandIndex1": [5, 6, 7],
            "RightHandIndex2": [6, 7, 8],
            "RightHandMiddle1": [9, 10, 11],
            "RightHandMiddle2": [10, 11, 12],
            "RightHandRing1": [13, 14, 15],
            "RightHandRing2": [14, 15, 16],
            "RightHandPinky1": [17, 18, 19],
            "RightHandPinky2": [18, 19, 20],
            # Left hand fingers (same indices, MediaPipe always gives 21 landmarks per hand)
            "LeftHandThumb1": [1, 2, 3],
            "LeftHandThumb2": [2, 3, 4],
            "LeftHandIndex1": [5, 6, 7],
            "LeftHandIndex2": [6, 7, 8],
            "LeftHandMiddle1": [9, 10, 11],
            "LeftHandMiddle2": [10, 11, 12],
            "LeftHandRing1": [13, 14, 15],
            "LeftHandRing2": [14, 15, 16],
            "LeftHandPinky1": [17, 18, 19],
            "LeftHandPinky2": [18, 19, 20],
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
            # Right hand fingers
            "RightHandThumb1": 2.0,
            "RightHandThumb2": 2.0,
            "RightHandIndex1": 2.0,
            "RightHandIndex2": 2.0,
            "RightHandMiddle1": 2.0,
            "RightHandMiddle2": 2.0,
            "RightHandRing1": 2.0,
            "RightHandRing2": 2.0,
            "RightHandPinky1": 2.0,
            "RightHandPinky2": 2.0,
            # Left hand fingers
            "LeftHandThumb1": 2.0,
            "LeftHandThumb2": 2.0,
            "LeftHandIndex1": 2.0,
            "LeftHandIndex2": 2.0,
            "LeftHandMiddle1": 2.0,
            "LeftHandMiddle2": 2.0,
            "LeftHandRing1": 2.0,
            "LeftHandRing2": 2.0,
            "LeftHandPinky1": 2.0,
            "LeftHandPinky2": 2.0,
        }

    def get_capabilities(self):
        return {
            'face': False,
            'hands': True,
        }

    def get_axis_corrections(self):
        from mathutils import Euler
        # Special handling for thumb to make it move more naturally
        # For thumb, we use a different rotation pattern to make it more natural
        # For other fingers, we invert the x-axis to make them bend correctly
        return {
            # Right hand thumb - special handling for more natural movement
            **{f'mixamorig:RightHandThumb{i}': lambda e: Euler((-e.x, -e.y, e.z)) for i in range(1, 4)},
            # Right hand other fingers
            **{f'mixamorig:RightHandIndex{i}': lambda e: Euler((-e.x, e.y, e.z)) for i in range(1, 4)},
            **{f'mixamorig:RightHandMiddle{i}': lambda e: Euler((-e.x, e.y, e.z)) for i in range(1, 4)},
            **{f'mixamorig:RightHandRing{i}': lambda e: Euler((-e.x, e.y, e.z)) for i in range(1, 4)},
            **{f'mixamorig:RightHandPinky{i}': lambda e: Euler((-e.x, e.y, e.z)) for i in range(1, 4)},
            # Left hand thumb - special handling for more natural movement
            **{f'mixamorig:LeftHandThumb{i}': lambda e: Euler((-e.x, -e.y, e.z)) for i in range(1, 4)},
            # Left hand other fingers
            **{f'mixamorig:LeftHandIndex{i}': lambda e: Euler((-e.x, e.y, e.z)) for i in range(1, 4)},
            **{f'mixamorig:LeftHandMiddle{i}': lambda e: Euler((-e.x, e.y, e.z)) for i in range(1, 4)},
            **{f'mixamorig:LeftHandRing{i}': lambda e: Euler((-e.x, e.y, e.z)) for i in range(1, 4)},
            **{f'mixamorig:LeftHandPinky{i}': lambda e: Euler((-e.x, e.y, e.z)) for i in range(1, 4)},
        }

    def get_hand_remap_table(self):
        """
        Returns remap tables for all hand joints (both hands).
        Each entry is a tuple: (input_range, output_range)

        We use more restrictive output ranges to prevent fingers from going through the palm
        when moved too fast or too much. This acts as a soft constraint.
        """
        # Standard input range for all fingers
        wide_in = (0, 100)

        # More restrictive output ranges to prevent fingers from going through the palm
        # First joints (closest to palm) have more limited movement
        first_joint_out = (0, 0.7)  # More limited range for first joints
        middle_joint_out = (0, 0.8)  # Slightly more range for middle joints
        tip_joint_out = (0, 0.9)    # Most range for tip joints

        # Special range for thumb which needs more freedom
        thumb_first_out = (0, 0.8)
        thumb_other_out = (0, 0.9)

        return {
            # Right hand with constrained ranges
            "RightHandThumb1.R":  (wide_in, thumb_first_out),
            "RightHandThumb2.R":  (wide_in, thumb_other_out),
            "RightHandThumb3.R":  (wide_in, thumb_other_out),
            "RightHandIndex1.R":  (wide_in, first_joint_out),
            "RightHandIndex2.R":  (wide_in, middle_joint_out),
            "RightHandIndex3.R":  (wide_in, tip_joint_out),
            "RightHandMiddle1.R": (wide_in, first_joint_out),
            "RightHandMiddle2.R": (wide_in, middle_joint_out),
            "RightHandMiddle3.R": (wide_in, tip_joint_out),
            "RightHandRing1.R":   (wide_in, first_joint_out),
            "RightHandRing2.R":   (wide_in, middle_joint_out),
            "RightHandRing3.R":   (wide_in, tip_joint_out),
            "RightHandPinky1.R":  (wide_in, first_joint_out),
            "RightHandPinky2.R":  (wide_in, middle_joint_out),
            "RightHandPinky3.R":  (wide_in, tip_joint_out),

            # Left hand with constrained ranges
            "LeftHandThumb1.L":  (wide_in, thumb_first_out),
            "LeftHandThumb2.L":  (wide_in, thumb_other_out),
            "LeftHandThumb3.L":  (wide_in, thumb_other_out),
            "LeftHandIndex1.L":  (wide_in, first_joint_out),
            "LeftHandIndex2.L":  (wide_in, middle_joint_out),
            "LeftHandIndex3.L":  (wide_in, tip_joint_out),
            "LeftHandMiddle1.L": (wide_in, first_joint_out),
            "LeftHandMiddle2.L": (wide_in, middle_joint_out),
            "LeftHandMiddle3.L": (wide_in, tip_joint_out),
            "LeftHandRing1.L":   (wide_in, first_joint_out),
            "LeftHandRing2.L":   (wide_in, middle_joint_out),
            "LeftHandRing3.L":   (wide_in, tip_joint_out),
            "LeftHandPinky1.L":  (wide_in, first_joint_out),
            "LeftHandPinky2.L":  (wide_in, middle_joint_out),
            "LeftHandPinky3.L":  (wide_in, tip_joint_out),
        }
