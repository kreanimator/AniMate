#!/bin/bash
set -e

# Clean up any previous build
rm -rf animate_addon_dist animate_addon.zip

# Create a new dist directory
mkdir animate_addon_dist

# Copy the main addon and dependencies
cp -r animate_addon animate_addon_dist/
cp -r rig animate_addon_dist/
cp -r data animate_addon_dist/
# Add any other folders you need, e.g.:
# cp -r utils animate_addon_dist/
# cp -r examples animate_addon_dist/

# (Optional) Copy README, license, etc.
# cp README.md animate_addon_dist/
# cp LICENSE animate_addon_dist/

# Zip it up
cd animate_addon_dist
zip -r ../animate_addon.zip .
cd ..

# Clean up dist directory
rm -rf animate_addon_dist

echo "Created animate_addon.zip. Install this in Blender via Edit > Preferences > Add-ons > Install." 