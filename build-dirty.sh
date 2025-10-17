#!/usr/bin/env nix
#!nix develop --command bash
set -euo pipefail

# Usage: ./build-dirty.sh <keyboard> [--flash]
#        ./build-dirty.sh --update <dependency>
#        ./build-dirty.sh --update-all
# Example: ./build-dirty.sh crutch
# Example: ./build-dirty.sh crutch --flash
# Example: ./build-dirty.sh --update zmk
# Example: ./build-dirty.sh --update-all

if [ $# -lt 1 ]; then
    echo "Usage: $0 <keyboard> [--flash]"
    echo "       $0 --update <dependency>"
    echo "       $0 --update-all"
    echo ""
    echo "Examples:"
    echo "  $0 crutch              # Build crutch keyboard"
    echo "  $0 crutch --flash      # Build and flash"
    echo "  $0 --update zmk        # Update zmk dependency"
    echo "  $0 --update-all        # Update all dependencies"
    exit 1
fi

# Handle update commands
if [ "$1" = "--update-all" ]; then
    REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    cd "$REPO_ROOT"

    if [ ! -d ".west" ]; then
        echo "Error: West workspace not initialized. Build a keyboard first."
        exit 1
    fi

    echo "Updating all west dependencies..."
    west update
    echo "Update complete!"
    exit 0
fi

if [ "$1" = "--update" ]; then
    if [ $# -lt 2 ]; then
        echo "Error: --update requires a dependency name"
        echo "Usage: $0 --update <dependency>"
        echo "Example: $0 --update zmk"
        exit 1
    fi

    DEPENDENCY="$2"
    REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    cd "$REPO_ROOT"

    if [ ! -d ".west" ]; then
        echo "Error: West workspace not initialized. Build a keyboard first."
        exit 1
    fi

    echo "Updating west dependency: $DEPENDENCY..."
    west update "$DEPENDENCY"
    echo "Update complete!"
    exit 0
fi

KEYBOARD="$1"
FLASH=false

if [ $# -gt 1 ] && [ "$2" = "--flash" ]; then
    FLASH=true
fi

# Map keyboard name to board and shield
case "$KEYBOARD" in
    crutch)
        BOARD="seeeduino_xiao_ble"
        SHIELD="crutch rgbled_adapter"
        SHIELD_DIR="boards/crutch/shield"
        ;;
    allium)
        BOARD="nice_nano_v2"
        SHIELD="allium"
        SHIELD_DIR="boards/allium/shield"
        ;;
    *)
        echo "Unknown keyboard: $KEYBOARD"
        echo "Add configuration for this keyboard in the script"
        exit 1
        ;;
esac

# Ensure we're in the repo root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

# Check if west workspace is initialized
if [ ! -d ".west" ]; then
    echo "Initializing west workspace..."
    west init -l config
    echo "Updating west dependencies (this may take a while)..."
    west update
fi

# Check if Zephyr exists
if [ ! -d "zephyr" ]; then
    echo "Error: Zephyr not found. Run 'nix develop -c west update' first"
    exit 1
fi

echo "Building $KEYBOARD (board: $BOARD, shield: $SHIELD)..."

# Use separate build directory for west builds
BUILD_DIR="$REPO_ROOT/build-west/$KEYBOARD"

# Prepare shield directory structure for west (like nix build does)
echo "Preparing shield structure..."
WEST_CONFIG="$BUILD_DIR/config"
mkdir -p "$WEST_CONFIG/boards/shields"

# Copy config files
cp -r "$REPO_ROOT/config"/* "$WEST_CONFIG/"

# Copy shield
cp -r "$REPO_ROOT/boards/$KEYBOARD/shield" "$WEST_CONFIG/boards/shields/$KEYBOARD"

# Copy keymap and conf to config if they exist
if [ -f "$REPO_ROOT/boards/$KEYBOARD/$KEYBOARD.keymap" ]; then
    cp "$REPO_ROOT/boards/$KEYBOARD/$KEYBOARD.keymap" "$WEST_CONFIG/"
fi
if [ -f "$REPO_ROOT/boards/$KEYBOARD/$KEYBOARD.conf" ]; then
    cp "$REPO_ROOT/boards/$KEYBOARD/$KEYBOARD.conf" "$WEST_CONFIG/"
fi

# Generate .dtsi from .chars files (like nix build does)
for chars_file in "$WEST_CONFIG"/*.chars; do
    if [ -f "$chars_file" ]; then
        basename="${chars_file%.chars}"
        dtsi_file="${basename}.dtsi"
        python3 "$REPO_ROOT/helpers/genunicode.py" < "$chars_file" > "$dtsi_file"
        rm "$chars_file"
    fi
done

# Build with west
export ZEPHYR_BASE=$REPO_ROOT/zephyr
west build -d $BUILD_DIR/build -b $BOARD -s zmk/app -- \
    -DSHIELD="$SHIELD" \
    -DZMK_CONFIG=$WEST_CONFIG \
    -DZephyr_DIR=$REPO_ROOT/zephyr/share/zephyr-package/cmake

echo ""
echo "Build complete!"
echo "Firmware: $BUILD_DIR/build/zephyr/zmk.uf2"

if [ "$FLASH" = true ]; then
    echo ""
    echo "Flashing firmware..."
    west flash -d $BUILD_DIR/build
fi
