# AniMate - Blender Motion Capture Plugin

A Blender plugin for real-time motion capture and animation of humanoid rigs using MediaPipe.

## Features

- Real-time motion capture using MediaPipe
- Support for full body tracking
- Face tracking and expression mapping
- Hand tracking and finger animation
- Automatic bone mapping and retargeting
- Smooth motion interpolation

## Project Status

🚧 **Under Development**

Currently implementing:
- Core motion capture functionality
- Bone mapping system
- Basic retargeting

## Requirements

- Blender 3.0 or higher
- Python 3.7+
- MediaPipe
- NumPy
- OpenCV

## Installation

1. Clone this repository:
```bash
git clone https://github.com/kreanimator/AniMate.git
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

3. Install the plugin in Blender:
   - Open Blender
   - Go to Edit > Preferences > Add-ons
   - Click "Install" and select the `__init__.py` file from this repository
   - Enable the plugin

## Usage

1. Open Blender and load your humanoid rig
2. Enable the AniMate plugin
3. Select your armature in the scene
4. Click "Start Capture" in the AniMate panel
5. Position yourself in front of the camera
6. The rig will follow your movements in real-time

## Project Structure

```
AniMate/
├── rig/                    # Core rigging functionality
│   ├── blender_mapper.py   # Blender-specific bone mapping
│   ├── retargeting.py      # Motion retargeting logic
│   └── mappings/          # Bone mapping configurations
├── utils/                  # Utility functions
├── tests/                  # Test files
└── data/                   # Sample data and configurations
```

## Development

### Setting up Development Environment

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

### Testing

- Use Blender's Python console for quick testing
- Run unit tests: `python -m pytest tests/`
- For visual testing, use the test rig in `tests/test_rig.blend`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details 