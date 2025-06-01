#!/bin/bash

echo "🔎 Starting Blender dependency installer..."

# Enable extended globbing and nullglob for wildcard expansion
shopt -s nullglob

# Function to check if Blender exists and is executable
find_blender() {
    echo "🔍 Checking paths for Blender..."
    for p in "$@"; do
        echo "🔍 Checking: $p"
        if [ -x "$p" ]; then
            echo "✅ Found Blender at: $p"
            BLENDER_PATH="$p"
            return 0
        fi
    done
    return 1
}

# Start with empty Blender path
BLENDER_PATH=""

# Try 'which'
BLENDER_PATH=$(which blender 2>/dev/null)
if [ -n "$BLENDER_PATH" ] && [ -x "$BLENDER_PATH" ]; then
    echo "✅ Found Blender via PATH: $BLENDER_PATH"
else
    echo "🔍 'which blender' did not find a valid executable. Expanding search paths..."

    # Expanded Snap/Flatpak/other paths
    SNAP_PATHS=()
    for d in "$HOME"/snap/blender-* "$HOME"/snap/blender-*/*; do
        if [ -d "$d" ]; then
            if [ -x "$d/blender" ]; then
                SNAP_PATHS+=("$d/blender")
            fi
        fi
    done

    echo "🔍 Expanded SNAP_PATHS: ${SNAP_PATHS[*]}"

    # Common search paths
    SEARCH_PATHS=(
        "/snap/bin/blender"
        "/var/lib/flatpak/app/org.blender.Blender/current/active/files/bin/blender"
        "/usr/bin/blender"
        "/usr/local/bin/blender"
        "/opt/blender/blender"
        "$HOME/blender/blender"
        "${SNAP_PATHS[@]}"
        "/Applications/Blender.app/Contents/MacOS/Blender"
        "/mnt/c/Program Files/Blender Foundation/Blender/blender.exe"
    )
    
    find_blender "${SEARCH_PATHS[@]}"
fi

shopt -u nullglob

# If not found, suggest Snap/apt install
if [ -z "$BLENDER_PATH" ]; then
    echo "❌ Blender not found automatically."
    echo "💡 You can install Blender with: sudo snap install blender  OR sudo apt install blender"
    read -rp "Please enter the full path to your Blender executable: " BLENDER_PATH
    if [ ! -x "$BLENDER_PATH" ]; then
        echo "❌ Invalid Blender path provided: $BLENDER_PATH"
        exit 1
    fi
fi

echo "🎉 Using Blender executable: $BLENDER_PATH"

# Get Blender's Python path
echo "🔎 Getting Blender's Python interpreter path..."
BLENDER_PYTHON=$("$BLENDER_PATH" --background --python-expr "import sys; print(sys.executable)" 2>&1 | tee /dev/stderr | tail -n 1)

if [ ! -x "$BLENDER_PYTHON" ]; then
    echo "❌ Could not determine Blender's Python interpreter."
    exit 1
fi

echo "🎉 Using Blender Python: $BLENDER_PYTHON"

# Get Blender's site-packages directory
BLENDER_SITE_PACKAGES=$("$BLENDER_PATH" --background --python-expr "import site; print(site.getsitepackages()[0])" 2>/dev/null | tail -n 1)
echo "📦 Using Blender site-packages: $BLENDER_SITE_PACKAGES"

# Remove user site-packages from Blender's sys.path (for this install session)
export PYTHONNOUSERSITE=1

# Ensure pip and upgrade
echo "🔎 Ensuring pip is installed/upgraded..."
"$BLENDER_PYTHON" -m ensurepip --upgrade
"$BLENDER_PYTHON" -m pip install --upgrade pip

# Install requirements
if [ -f requirements.txt ]; then
    echo "🔎 Installing dependencies from requirements.txt..."
    "$BLENDER_PYTHON" -m pip install --upgrade --force-reinstall --no-user --target="$BLENDER_SITE_PACKAGES" -r requirements.txt
    echo "✅ All dependencies installed for Blender's Python!"
else
    echo "❌ requirements.txt not found! Please provide the file."
    exit 1
fi

# Manual installation of packaging
echo "🔎 Installing packaging dependency manually..."
/home/vall/snap/blender-4.3.2-linux-x64/4.3/python/bin/python3.11 -m pip install --target=/home/vall/snap/blender-4.3.2-linux-x64/4.3/python/lib/python3.11/site-packages packaging
