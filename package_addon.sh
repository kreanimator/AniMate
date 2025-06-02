#!/bin/bash
set -e

# Clean up any previous build
rm -rf animate_addon_dist animate_addon.zip

# Create the dist directory
mkdir animate_addon_dist

# Copy the new_structure as a subdirectory
cp -r AniMate animate_addon_dist/

# Rename the folder inside the zip to animate_addon
mv animate_addon_dist/AniMate animate_addon_dist/animate_addon

# Zip it up
cd animate_addon_dist
zip -r ../animate_addon.zip animate_addon
cd ..

# Clean up dist directory
rm -rf animate_addon_dist

echo "Created animate_addon.zip. Install this in Blender via Edit > Preferences > Add-ons > Install."
