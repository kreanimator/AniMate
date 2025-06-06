import bpy
from bpy.types import Panel
from .properties import AniMateProperties
from ..utils.version import get_addon_version_string

def is_area_valid(area):
    """
    Check if an area is still valid by trying to access its properties.

    Args:
        area: The area to check

    Returns:
        bool: True if the area is valid, False otherwise
    """
    try:
        # Try to access a property of the area
        _ = area.type
        return True
    except ReferenceError:
        return False

def split_and_set_image_editor(img_name):
    """
    Split the current area and set one half to an image editor with the specified image.

    Args:
        img_name: The name of the image to display in the image editor
    """
    try:
        window = bpy.context.window
        screen = window.screen

        # Join all areas into the largest one
        areas = list(screen.areas)
        if len(areas) > 1:
            main_area = max(areas, key=lambda a: a.width * a.height)
            for area in list(areas):  # Use a copy to avoid modification during iteration
                if area != main_area:
                    # Check if both areas are still valid
                    if not is_area_valid(area) or not is_area_valid(main_area):
                        continue

                    # Double-check that both areas are still valid before joining
                    if is_area_valid(area) and is_area_valid(main_area):
                        try:
                            # Use C-style override context
                            with bpy.context.temp_override(window=window, screen=screen, area=area):
                                bpy.ops.screen.area_join()
                        except Exception as e:
                            print(f"[AniMate] Area join failed in inner try block: {e}")
                    else:
                        print(f"[AniMate] One or both areas are no longer valid, skipping join operation")

        # Now only one area, split it by calling the operator directly
        try:
            # Call area_split directly without override as in the original implementation
            bpy.ops.screen.area_split(direction='VERTICAL', factor=0.5)

            # After splitting, get the areas sorted by x position
            areas = sorted(screen.areas, key=lambda a: a.x)
            if len(areas) >= 2:
                left_area, right_area = areas[0], areas[1]
                left_area.type = 'IMAGE_EDITOR'
                for space in left_area.spaces:
                    if space.type == 'IMAGE_EDITOR':
                        space.image = bpy.data.images[img_name]
                        break
                right_area.type = 'VIEW_3D'
            else:
                print("[AniMate] Area split succeeded but didn't create enough areas.")
        except Exception as e:
            print(f"[AniMate] Area split failed: {e}. Switching largest area to IMAGE_EDITOR.")
            try:
                max_area = max(screen.areas, key=lambda a: a.width * a.height)
                max_area.type = 'IMAGE_EDITOR'
                for space in max_area.spaces:
                    if space.type == 'IMAGE_EDITOR':
                        space.image = bpy.data.images[img_name]
                        break
            except Exception as e2:
                print(f"[AniMate] Failed to set up image editor: {e2}")

        return None  # Only run once
    except Exception as e:
        print(f"[AniMate] Error in split_and_set_image_editor: {e}")
        return None

def merge_view3d_areas(window, screen, view3d_areas):
    """
    Merge multiple VIEW_3D areas into the largest one.

    Args:
        window: The current Blender window
        screen: The current Blender screen
        view3d_areas: List of VIEW_3D areas to merge
    """
    if len(view3d_areas) <= 1:
        print("[AniMate] Only one VIEW_3D area found, no merging needed.")
        return

    # Make a copy of the list to avoid modification during iteration
    view3d_areas = list(view3d_areas)

    # Get the largest VIEW_3D area
    main_area = max(view3d_areas, key=lambda a: a.width * a.height)
    print(f"[AniMate] Main area for merging: {main_area}, size: {main_area.width}x{main_area.height}")

    # Join all other VIEW_3D areas into the main area
    # Make a copy of the list to avoid modification during iteration
    for area in list(view3d_areas):
        if area != main_area:
            try:
                # Check if the area is still valid
                if not is_area_valid(area):
                    continue

                # Check if the main area is still valid
                if not is_area_valid(main_area):
                    # Find a new main area from the remaining areas
                    remaining_areas = [a for a in screen.areas if a.type == 'VIEW_3D' and a != area]
                    if not remaining_areas:
                        break  # No more areas to join with
                    main_area = max(remaining_areas, key=lambda a: a.width * a.height)

                # Double-check that both areas are still valid before joining
                if is_area_valid(area) and is_area_valid(main_area):
                    try:
                        # Use C-style override context
                        with bpy.context.temp_override(window=window, screen=screen, area=area):
                            bpy.ops.screen.area_join()
                        print("[AniMate] Successfully merged VIEW_3D areas.")
                    except Exception as e:
                        print(f"[AniMate] Area join failed in inner try block: {e}")
                else:
                    print(f"[AniMate] One or both areas are no longer valid, skipping join operation")
            except Exception as e:
                print(f"[AniMate] Failed to merge VIEW_3D areas: {e}")

def close_image_editor():
    """
    Close the image editor preview while preserving the original layout.
    This should be called when motion capture is stopped.
    """
    try:
        window = bpy.context.window
        screen = window.screen

        # Find the IMAGE_EDITOR area (ensure they are valid)
        image_editor_areas = [area for area in screen.areas if area.type == 'IMAGE_EDITOR' and is_area_valid(area)]

        if not image_editor_areas:
            print("[AniMate] No image editor found to close.")
            return

        # Find a VIEW_3D area to merge with (ensure they are valid)
        view3d_areas = [area for area in screen.areas if area.type == 'VIEW_3D' and is_area_valid(area)]

        if not view3d_areas:
            # If no VIEW_3D area exists, convert the image editor to VIEW_3D
            for area in image_editor_areas:
                try:
                    area.type = 'VIEW_3D'
                    print(f"[AniMate] Converted area {area} to VIEW_3D")
                except Exception as e:
                    print(f"[AniMate] Failed to convert area to VIEW_3D: {e}")
            print("[AniMate] Converted image editor to 3D view.")

            # Now we need to check if we have multiple VIEW_3D areas and merge them
            view3d_areas = [area for area in screen.areas if area.type == 'VIEW_3D' and is_area_valid(area)]
            print(f"[AniMate] After conversion, found {len(view3d_areas)} VIEW_3D areas")

            if len(view3d_areas) > 1:
                try:
                    print(f"[AniMate] Merging {len(view3d_areas)} VIEW_3D areas...")
                    merge_view3d_areas(window, screen, view3d_areas)
                except Exception as e:
                    print(f"[AniMate] Failed to merge VIEW_3D areas: {e}")

            # Don't return here, continue with the rest of the function to ensure all areas are properly merged

        # Update the list of VIEW_3D areas in case it changed (ensure they are valid)
        view3d_areas = [area for area in screen.areas if area.type == 'VIEW_3D' and is_area_valid(area)]

        # If there are no VIEW_3D areas, we can't continue with joining
        if not view3d_areas:
            print("[AniMate] No VIEW_3D areas found after conversion, can't continue with joining.")
            return

        # Get the largest VIEW_3D area
        main_area = max(view3d_areas, key=lambda a: a.width * a.height)

        # Join the image editor areas with the main VIEW_3D area
        # Make a copy of the list to avoid modification during iteration
        print(f"[AniMate] Joining {len(image_editor_areas)} image editor areas with main VIEW_3D area")
        for area in list(image_editor_areas):
            try:
                # Check if the area is still valid
                if not is_area_valid(area):
                    print(f"[AniMate] Area {area} is no longer valid, skipping")
                    continue

                # Check if the main area is still valid
                if not is_area_valid(main_area):
                    print(f"[AniMate] Main area {main_area} is no longer valid, finding a new one")
                    # Find a new main area (ensure they are valid)
                    view3d_areas = [a for a in screen.areas if a.type == 'VIEW_3D' and is_area_valid(a)]
                    if not view3d_areas:
                        # No VIEW_3D areas left, just convert this area
                        print(f"[AniMate] No VIEW_3D areas left, converting {area} to VIEW_3D")
                        area.type = 'VIEW_3D'
                        continue
                    main_area = max(view3d_areas, key=lambda a: a.width * a.height)
                    print(f"[AniMate] New main area: {main_area}, size: {main_area.width}x{main_area.height}")

                # Double-check that both areas are still valid before joining
                if is_area_valid(area) and is_area_valid(main_area):
                    try:
                        # Use C-style override context
                        with bpy.context.temp_override(window=window, screen=screen, area=area):
                            bpy.ops.screen.area_join()
                        print("[AniMate] Successfully joined image editor with 3D view.")
                    except Exception as e:
                        print(f"[AniMate] Area join failed in inner try block: {e}")
                        # If joining fails, convert to VIEW_3D
                        area.type = 'VIEW_3D'
                        print(f"[AniMate] Converted area to VIEW_3D after join failure")
                else:
                    print(f"[AniMate] One or both areas are no longer valid, skipping join operation")
                    # If the area is still valid, convert it to VIEW_3D
                    if is_area_valid(area):
                        area.type = 'VIEW_3D'
                        print(f"[AniMate] Converted area to VIEW_3D because main area is invalid")
            except Exception as e:
                try:
                    # If joining fails, just convert to VIEW_3D if the area is still valid
                    if is_area_valid(area):
                        print(f"[AniMate] Area join failed: {e}, converting {area} to VIEW_3D")
                        area.type = 'VIEW_3D'

                        # After converting to VIEW_3D, we need to merge it with other VIEW_3D areas
                        # This is crucial to avoid ending up with multiple VIEW_3D areas
                        # Wait a moment to ensure the area type change is processed
                        view3d_areas = [a for a in screen.areas if a.type == 'VIEW_3D' and is_area_valid(a)]
                        if len(view3d_areas) > 1:
                            print(f"[AniMate] After conversion, found {len(view3d_areas)} VIEW_3D areas, merging them...")
                            # Create a new window and screen reference to ensure we have the latest state
                            window = bpy.context.window
                            screen = window.screen
                            merge_view3d_areas(window, screen, view3d_areas)
                except Exception as e2:
                    print(f"[AniMate] Failed to convert area to VIEW_3D: {e2}")

        # Check if we need to merge any remaining VIEW_3D areas
        try:
            # Always check for and merge VIEW_3D areas after converting or joining
            # Create a new window and screen reference to ensure we have the latest state
            window = bpy.context.window
            screen = window.screen
            view3d_areas = [area for area in screen.areas if area.type == 'VIEW_3D' and is_area_valid(area)]
            if len(view3d_areas) > 1:
                print(f"[AniMate] Found {len(view3d_areas)} VIEW_3D areas, merging them...")
                merge_view3d_areas(window, screen, view3d_areas)
            else:
                print(f"[AniMate] Only found {len(view3d_areas)} VIEW_3D area, no merging needed.")
        except Exception as e:
            print(f"[AniMate] Failed to merge VIEW_3D areas: {e}")

        print("[AniMate] Preview window closed while preserving original layout.")
    except Exception as e:
        print(f"[AniMate] Error in close_image_editor: {e}")

class AniMateMainPanel(Panel):
    bl_label = "AniMate"
    bl_idname = "ANIMATE_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AniMate'

    def draw(self, context):
        layout = self.layout
        props = context.scene.animate_properties
        # Display version/build info
        layout.label(text=f"AniMate Version: {get_addon_version_string()}")
        layout.prop(props, "rig_type")
        layout.prop(props, "target_armature")
        box = layout.box()
        box.label(text="Detection Settings:")
        box.prop(props, "enable_pose")
        box.prop(props, "enable_face")
        box.prop(props, "enable_hands")
        box.prop(props, "camera_mirrored")
        box.prop(props, "show_camera_preview")
        box.prop(props, "debug_mode")
        layout.separator()
        row = layout.row()
        if getattr(context.scene, 'animate_running', False):
            row.operator("animate.stop_capture", text="Stop Capture", icon='CANCEL')
        else:
            row.operator("animate.start_capture", text="Start Capture", icon='REC') 
