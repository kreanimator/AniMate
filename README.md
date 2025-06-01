# AniMate

A Blender plugin for animating humanoid rigs using motion capture data from MediaPipe.

## Features

- Real-time motion capture using MediaPipe
- Support for pose, face, and hand tracking
- Configurable bone mappings
- Test rigs for development and testing
- Modular and extensible architecture

## Project Status

🚧 **Under Development** 🚧

The project is currently in active development. Core functionality is implemented but may have bugs or missing features.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AniMate.git
cd AniMate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create a ZIP file for the Blender addon:
```bash
zip -r animate_addon.zip animate_addon
```

4. Install the Blender addon:
   - Open Blender
   - Go to Edit > Preferences > Add-ons
   - Click "Install" and select the `animate_addon.zip` file you just created
   - Enable the addon by checking the box next to "Animation: AniMate"

## Project Structure

```
AniMate/
├── animate_addon/         # Blender addon files
│   └── __init__.py       # Addon initialization and UI
├── data/                  # Data and configuration files
│   ├── bone_mappings.py   # MediaPipe to Blender bone mappings
│   ├── landmark_structure.py # MediaPipe landmark definitions
│   └── test_rigs.py       # Test rig configurations
├── examples/              # Example scripts
│   └── live_capture.py    # Live motion capture example
├── rig/                   # Blender rig functionality
│   ├── blender_mapper.py  # Blender-specific rig mapping
│   └── retargeting.py     # Retargeting functionality
├── tests/                 # Test scripts
│   ├── test_detection.py  # MediaPipe detection tests
│   └── test_rig.py        # Rig functionality tests
├── utils/                 # Utility functions
│   └── detection.py       # MediaPipe detection module
└── README.md             # This file
```

## Usage

### In Blender

1. Open Blender and load your humanoid rig
2. In the 3D Viewport, open the sidebar (N key)
3. Go to the "AniMate" tab
4. Select your armature in the "Target Armature" field
5. Configure detection settings (pose, face, hands)
6. Click "Start Capture" to begin motion capture

### Testing Detection

To test the MediaPipe detection functionality without Blender:

```bash
python tests/test_detection.py
```

Controls:
- 'p' - Toggle pose detection
- 'f' - Toggle face detection
- 'h' - Toggle hand detection
- 'ESC' - Exit

## Development

### Adding New Features

1. Detection:
   - Add new detection types in `utils/detection.py`
   - Update bone mappings in `data/bone_mappings.py`

2. Rig Support:
   - Add new rig configurations in `data/test_rigs.py`
   - Implement rig-specific mapping in `rig/blender_mapper.py`

3. Addon UI:
   - Modify `animate_addon/__init__.py` to add new UI elements
   - Add new operators and properties as needed

### Testing

1. Run detection tests:
```bash
python tests/test_detection.py
```

2. Run rig tests:
```bash
python tests/test_rig.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- MediaPipe for the motion capture technology
- Blender for the 3D animation platform
