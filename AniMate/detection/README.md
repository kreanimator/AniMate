# detection

This module contains the MediaPipe-based detection logic for the AniMate Blender addon. It provides real-time tracking of pose, hands, and face landmarks using MediaPipe's machine learning models.

## Components

- `MediaPipeDetector`: Main detector class that handles:
  - Pose tracking (body landmarks)
  - Hand tracking (left and right hand landmarks)
  - Face tracking (facial landmarks)
  - Holistic tracking (all of the above)

The detector can be configured to run in different modes ('pose', 'hands', 'face', or 'holistic') depending on the tracking needs. 