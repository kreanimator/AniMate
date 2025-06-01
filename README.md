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

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the Blender addon:
   - Open Blender
   - Go to Edit > Preferences > Add-ons
   - Click "Install" and select the `addon` folder from this repository

## Project Structure

```
AniMate/
├── data/                   # Data and configuration files
│   ├── bone_mappings.py    # MediaPipe to Blender bone mappings
│   ├── landmark_structure.py # MediaPipe landmark definitions
│   └── test_rigs.py        # Test rig configurations
├── examples/               # Example scripts
│   └── live_capture.py     # Live motion capture example
├── rig/                    # Blender rig functionality
│   ├── blender_mapper.py   # Blender-specific rig mapping
│   └── retargeting.py      # Retargeting functionality
├── tests/                  # Test scripts
│   ├── test_detection.py   # MediaPipe detection tests
│   └── test_rig.py         # Rig functionality tests
├── utils/                  # Utility functions
│   └── detection.py        # MediaPipe detection module
└── README.md              # This file
```

## Usage

### Testing Detection

To test the MediaPipe detection functionality:

```bash
python tests/test_detection.py
```

Controls:
- 'p' - Toggle pose detection
- 'f' - Toggle face detection
- 'h' - Toggle hand detection
- 'ESC' - Exit

### Live Motion Capture

To use the live motion capture with Blender:

1. Open Blender
2. Run the example script:
```bash
python examples/live_capture.py
```

## Development

### Adding New Features

1. Detection:
   - Add new detection types in `utils/detection.py`
   - Update bone mappings in `data/bone_mappings.py`

2. Rig Support:
   - Add new rig configurations in `data/test_rigs.py`
   - Implement rig-specific mapping in `rig/blender_mapper.py`

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