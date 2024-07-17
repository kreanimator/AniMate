__author__ = "Valentin Bakin"

"""
Rig package for handling the 3D rig and animation logic.
Contains:
- rig_mapper: Functions to map landmarks to the 3D rig
- animator: Functions to animate the rig based on landmarks
"""

from .rig_mapper import map_landmarks_to_rig
from .animator import animate_rig

__all__ = ["map_landmarks_to_rig", "animate_rig"]
