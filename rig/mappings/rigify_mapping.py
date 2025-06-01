"""
Rigify rig mapping implementation.
"""
from .base_mappings import BaseRigMapping

class RigifyMapping(BaseRigMapping):
    """Mapping implementation for Rigify rigs."""
    
    def get_pose_mapping(self):
        return {
            # Spine
            'spine': [11, 23],  # Shoulder to Hip
            'spine.001': [23, 24],  # Hip to Hip
            'spine.002': [24, 12],  # Hip to Shoulder
            
            # Head
            'neck': [11, 0],  # Shoulder to Nose
            'head': [0, 8],  # Nose to Forehead
            
            # Left Arm
            'shoulder.L': [11, 13],  # Shoulder to Elbow
            'upper_arm.L': [13, 15],  # Elbow to Wrist
            
            # Right Arm
            'shoulder.R': [12, 14],  # Shoulder to Elbow
            'upper_arm.R': [14, 16],  # Elbow to Wrist
            
            # Left Leg
            'thigh.L': [23, 25],  # Hip to Knee
            'shin.L': [25, 27],  # Knee to Ankle
            'foot.L': [27, 31],  # Ankle to Heel
            
            # Right Leg
            'thigh.R': [24, 26],  # Hip to Knee
            'shin.R': [26, 28],  # Knee to Ankle
            'foot.R': [28, 32],  # Ankle to Heel
        }
    
    def get_hand_mapping(self):
        return {
            # Thumb
            'thumb.01.L': [0, 1],
            'thumb.02.L': [1, 2],
            'thumb.03.L': [2, 3],
            
            # Index
            'f_index.01.L': [0, 5],
            'f_index.02.L': [5, 6],
            'f_index.03.L': [6, 7],
            
            # Middle
            'f_middle.01.L': [0, 9],
            'f_middle.02.L': [9, 10],
            'f_middle.03.L': [10, 11],
            
            # Ring
            'f_ring.01.L': [0, 13],
            'f_ring.02.L': [13, 14],
            'f_ring.03.L': [14, 15],
            
            # Pinky
            'f_pinky.01.L': [0, 17],
            'f_pinky.02.L': [17, 18],
            'f_pinky.03.L': [18, 19]
        }
    
    def get_face_mapping(self):
        return {
            'jaw': [152, 175],  # Jaw movement
            'eye.L': [33, 133],  # Left eye movement
            'eye.R': [362, 263],  # Right eye movement
        }
    
    def get_bone_hierarchy(self):
        return {
            "root": {
                "spine": {
                    "spine.001": {
                        "spine.002": {
                            "neck": {
                                "head": {
                                    "head.x": {}
                                }
                            }
                        }
                    }
                },
                "thigh.L": {
                    "shin.L": {
                        "foot.L": {
                            "toe.L": {
                                "toe.L.001": {}
                            }
                        }
                    }
                },
                "thigh.R": {
                    "shin.R": {
                        "foot.R": {
                            "toe.R": {
                                "toe.R.001": {}
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
                }
            }
        }
    
    def get_bone_rotation_limits(self):
        """Get the rotation limits for each bone in degrees."""
        return {
            'spine': {'x': (-30, 30), 'y': (-30, 30), 'z': (-30, 30)},
            'neck': {'x': (-30, 30), 'y': (-30, 30), 'z': (-30, 30)},
            'shoulder.L': {'x': (-90, 90), 'y': (-90, 90), 'z': (-90, 90)},
            'shoulder.R': {'x': (-90, 90), 'y': (-90, 90), 'z': (-90, 90)},
            # Add more bone limits as needed
        }
    
    def get_bone_scale_factors(self):
        """Get the scale factors for each bone."""
        return {
            'spine': 1.0,
            'neck': 1.0,
            'shoulder.L': 1.0,
            'shoulder.R': 1.0,
            # Add more bone scale factors as needed
        } 