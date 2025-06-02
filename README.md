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
git clone https://github.com/kreanimator/AniMate.git
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

## Manual Dependency Installation (for Snap/Flatpak/Custom Blender)

**Important:** If you are using Blender from Snap, Flatpak, or a custom build, you must manually install all dependencies from `requirements.txt` into Blender's Python environment.

### Steps:
1. Find Blender's Python executable:
   ```bash
   blender --background --python-expr "import sys; print(sys.executable)"
   # Example output: /home/youruser/snap/blender-4.3.2-linux-x64/4.3/python/bin/python3.11
   ```
2. Find Blender's site-packages directory:
   ```bash
   blender --background --python-expr "import site; print(site.getsitepackages()[0])"
   # Example output: /home/youruser/snap/blender-4.3.2-linux-x64/4.3/python/lib/python3.11/site-packages
   ```
3. For each dependency in `requirements.txt`, run:
   ```bash
   /path/to/blender/python/bin/python3.11 -m pip install --target=/path/to/blender/python/lib/python3.11/site-packages <package>
   # Example:
   /home/youruser/snap/blender-4.3.2-linux-x64/4.3/python/bin/python3.11 -m pip install --target=/home/youruser/snap/blender-4.3.2-linux-x64/4.3/python/lib/python3.11/site-packages packaging
   /home/youruser/snap/blender-4.3.2-linux-x64/4.3/python/bin/python3.11 -m pip install --target=/home/youruser/snap/blender-4.3.2-linux-x64/4.3/python/lib/python3.11/site-packages opencv-python
   /home/youruser/snap/blender-4.3.2-linux-x64/4.3/python/bin/python3.11 -m pip install --target=/home/youruser/snap/blender-4.3.2-linux-x64/4.3/python/lib/python3.11/site-packages mediapipe
   /home/youruser/snap/blender-4.3.2-linux-x64/4.3/python/bin/python3.11 -m pip install --target=/home/youruser/snap/blender-4.3.2-linux-x64/4.3/python/lib/python3.11/site-packages Pillow
   ```

**Note:** You must repeat this for every dependency in `requirements.txt`.

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

## Packaging and Installing the Addon in Blender

To install this addon in Blender, you need to package all required folders into a single zip file. Use the provided shell script:

1. Open a terminal in your project root.
2. Run:
   ```bash
   bash package_addon.sh
   ```
3. This will create `animate_addon.zip` in your project root.
4. In Blender, go to `Edit > Preferences > Add-ons > Install`, and select `animate_addon.zip`.
5. Enable the addon in the list.

**The script will include:**
- `animate_addon/` (main addon code)
- `rig/` (rig logic and mappings)
- `data/` (any data files needed)

If you add more dependencies (like `utils/` or `examples/`), uncomment the relevant lines in `package_addon.sh`.

## Test Scene for Blender Development

A sample Blender file is provided for development and testing:

- **data/sample_scene_with_mixamo_rig.blend**

This file contains a human mesh with a Mixamo rig and can be used as a test scene for AniMate development in Blender. Load this file to quickly test the addon with a compatible rig and mesh setup.
