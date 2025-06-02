"""
Rigify rig mapping implementation.
"""
from .base_mappings import BaseRigMapping
from mathutils import Vector, Matrix, Euler


class RigifyMapping(BaseRigMapping):
    """Mapping for Rigify rigs."""

    def get_bone_hierarchy(self):
        """Get the expected bone hierarchy for Rigify rigs."""
        return {
            "spine": {
                "spine.001": {
                    "spine.002": {
                        "spine.003": {
                            "spine.004": {
                                "spine.005": {
                                    "spine.006": {}
                                }
                            },
                            "shoulder.R": {
                                "upper_arm.R": {
                                    "forearm.R": {
                                        "hand.R": {
                                            "thumb.01.R": {
                                                "thumb.02.R": {
                                                    "thumb.03.R": {}
                                                }
                                            },
                                            "f_index.01.R": {
                                                "f_index.02.R": {
                                                    "f_index.03.R": {}
                                                }
                                            },
                                            "f_middle.01.R": {
                                                "f_middle.02.R": {
                                                    "f_middle.03.R": {}
                                                }
                                            },
                                            "f_ring.01.R": {
                                                "f_ring.02.R": {
                                                    "f_ring.03.R": {}
                                                }
                                            },
                                            "f_pinky.01.R": {
                                                "f_pinky.02.R": {
                                                    "f_pinky.03.R": {}
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "shoulder.L": {
                                "upper_arm.L": {
                                    "forearm.L": {
                                        "hand.L": {
                                            "thumb.01.L": {
                                                "thumb.02.L": {
                                                    "thumb.03.L": {}
                                                }
                                            },
                                            "f_index.01.L": {
                                                "f_index.02.L": {
                                                    "f_index.03.L": {}
                                                }
                                            },
                                            "f_middle.01.L": {
                                                "f_middle.02.L": {
                                                    "f_middle.03.L": {}
                                                }
                                            },
                                            "f_ring.01.L": {
                                                "f_ring.02.L": {
                                                    "f_ring.03.L": {}
                                                }
                                            },
                                            "f_pinky.01.L": {
                                                "f_pinky.02.L": {
                                                    "f_pinky.03.L": {}
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
            "spine": [23, 24],  # Left and right hip
            "spine.001": [23, 11],  # Hip to mid-spine
            "spine.002": [11, 12],  # Mid-spine to upper spine
            "spine.003": [12, 0],  # Upper spine to neck
            "spine.004": [0, 2],  # Neck to head
            "spine.005": [2, 8],  # Head to nose
            "shoulder.R": [11, 12],  # Spine to right shoulder
            "upper_arm.R": [12, 14],  # Shoulder to elbow
            "forearm.R": [14, 16],  # Elbow to wrist
            "shoulder.L": [11, 12],  # Spine to left shoulder
            "upper_arm.L": [12, 13],  # Shoulder to elbow
            "forearm.L": [13, 15],  # Elbow to wrist
        }

    def get_face_mapping(self):
        """Get the mapping between MediaPipe face landmarks and bone names."""
        return {
            "spine.005": [0, 1],  # Nose to forehead
            "spine.004": [1, 2],  # Forehead to chin
        }

    def get_hand_mapping(self):
        """Get the mapping between MediaPipe hand landmarks and bone names."""
        return {
            # Right hand
            "thumb.01.R": [0, 1],
            "thumb.02.R": [1, 2],
            "thumb.03.R": [2, 3],
            "f_index.01.R": [0, 5],
            "f_index.02.R": [5, 6],
            "f_index.03.R": [6, 7],
            "f_middle.01.R": [0, 9],
            "f_middle.02.R": [9, 10],
            "f_middle.03.R": [10, 11],
            "f_ring.01.R": [0, 13],
            "f_ring.02.R": [13, 14],
            "f_ring.03.R": [14, 15],
            "f_pinky.01.R": [0, 17],
            "f_pinky.02.R": [17, 18],
            "f_pinky.03.R": [18, 19],
            # Left hand
            "thumb.01.L": [0, 1],
            "thumb.02.L": [1, 2],
            "thumb.03.L": [2, 3],
            "f_index.01.L": [0, 5],
            "f_index.02.L": [5, 6],
            "f_index.03.L": [6, 7],
            "f_middle.01.L": [0, 9],
            "f_middle.02.L": [9, 10],
            "f_middle.03.L": [10, 11],
            "f_ring.01.L": [0, 13],
            "f_ring.02.L": [13, 14],
            "f_ring.03.L": [14, 15],
            "f_pinky.01.L": [0, 17],
            "f_pinky.02.L": [17, 18],
            "f_pinky.03.L": [18, 19],
        }

    def get_bone_rotation_limits(self):
        """Get rotation limits for each bone."""
        return {
            "spine": {"x": (-45, 45), "y": (-45, 45), "z": (-45, 45)},
            "spine.001": {"x": (-30, 30), "y": (-30, 30), "z": (-30, 30)},
            "spine.002": {"x": (-30, 30), "y": (-30, 30), "z": (-30, 30)},
            "spine.003": {"x": (-30, 30), "y": (-30, 30), "z": (-30, 30)},
            "spine.004": {"x": (-45, 45), "y": (-45, 45), "z": (-45, 45)},
            "spine.005": {"x": (-45, 45), "y": (-45, 45), "z": (-45, 45)},
            "shoulder.R": {"x": (-90, 90), "y": (-90, 90), "z": (-90, 90)},
            "upper_arm.R": {"x": (-90, 90), "y": (-90, 90), "z": (-90, 90)},
            "forearm.R": {"x": (-90, 90), "y": (-90, 90), "z": (-90, 90)},
            "shoulder.L": {"x": (-90, 90), "y": (-90, 90), "z": (-90, 90)},
            "upper_arm.L": {"x": (-90, 90), "y": (-90, 90), "z": (-90, 90)},
            "forearm.L": {"x": (-90, 90), "y": (-90, 90), "z": (-90, 90)},
        }

    def get_bone_scale_factors(self):
        """Get scale factors for each bone's rotation."""
        return {
            "spine": 1.0,
            "spine.001": 1.0,
            "spine.002": 1.0,
            "spine.003": 1.0,
            "spine.004": 1.0,
            "spine.005": 1.0,
            "shoulder.R": 1.0,
            "upper_arm.R": 1.0,
            "forearm.R": 1.0,
            "shoulder.L": 1.0,
            "upper_arm.L": 1.0,
            "forearm.L": 1.0,
        }

    def get_capabilities(self):
        """Get the capabilities of this rig type."""
        return {
            'face': True,  # Rigify supports face tracking
            'hands': True,
        } 