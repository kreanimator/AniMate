mapping
=======

This module contains all rig mapping logic for the AniMate Blender addon. Each mapping class defines the bone hierarchy, MediaPipe-to-bone mapping, rotation limits, scale factors, and axis corrections for a specific rig type.

Available mapping classes:

- ``MixamoMapping``: For Mixamo rigs
- ``RigifyMapping``: For Rigify rigs
- ``MayaMapping``: For Maya rigs (placeholder)

The ``RigMappingFactory`` provides a unified interface to create and query mappings by rig type. 