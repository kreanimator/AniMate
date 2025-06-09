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

def calculate_join_cursor_position(area1, area2):
    """
    Calculate the cursor position for joining two areas.
    The cursor position needs to be between the two areas.

    Args:
        area1: The first area
        area2: The second area

    Returns:
        tuple: (x, y) cursor position for the join operation
    """
    # Determine if areas are side by side or one above the other
    if area1.x < area2.x:
        # area1 is to the left of area2
        cursor_x = area1.x + area1.width
        cursor_y = area2.y + 2  # Add a small offset to avoid issues
    elif area1.x > area2.x:
        # area1 is to the right of area2
        cursor_x = area2.x + area2.width
        cursor_y = area1.y + 2
    elif area1.y < area2.y:
        # area1 is below area2
        cursor_x = area2.x + 2
        cursor_y = area1.y + area1.height
    else:
        # area1 is above area2
        cursor_x = area1.x + 2
        cursor_y = area2.y + area2.height

    return (cursor_x, cursor_y)

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
                            # Calculate the cursor position for joining
                            cursor_pos = calculate_join_cursor_position(area, main_area)
                            print(f"[AniMate] Joining areas with cursor at {cursor_pos}")

                            # Use C-style override context
                            with bpy.context.temp_override(window=window, screen=screen, area=area):
                                # Set the mouse cursor position
                                bpy.context.window.cursor_warp(cursor_pos[0], cursor_pos[1])
                                # Join the areas
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
    # Log the number of areas before merging
    print(f"[AniMate] Before merging: {len(view3d_areas)} VIEW_3D areas, {len(screen.areas)} total areas")

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
                    print(f"[AniMate] Area {area} is no longer valid, skipping")
                    continue

                # Check if the main area is still valid
                if not is_area_valid(main_area):
                    print(f"[AniMate] Main area {main_area} is no longer valid, finding a new one")
                    # Find a new main area from the remaining areas
                    remaining_areas = [a for a in screen.areas if a.type == 'VIEW_3D' and a != area]
                    if not remaining_areas:
                        print("[AniMate] No more areas to join with, breaking")
                        break  # No more areas to join with
                    main_area = max(remaining_areas, key=lambda a: a.width * a.height)
                    print(f"[AniMate] New main area: {main_area}, size: {main_area.width}x{main_area.height}")

                # Double-check that both areas are still valid before joining
                if is_area_valid(area) and is_area_valid(main_area):
                    print(f"[AniMate] Attempting to join {area} with main area {main_area}")
                    try:
                        # Calculate the cursor position for joining
                        cursor_pos = calculate_join_cursor_position(area, main_area)
                        print(f"[AniMate] Joining VIEW_3D areas with cursor at {cursor_pos}")

                        # Count areas before joining
                        areas_before = len([a for a in screen.areas if is_area_valid(a)])

                        # Use C-style override context
                        with bpy.context.temp_override(window=window, screen=screen, area=area):
                            # Set the mouse cursor position
                            bpy.context.window.cursor_warp(cursor_pos[0], cursor_pos[1])
                            # Join the areas
                            bpy.ops.screen.area_join()

                        # Count areas after joining
                        areas_after = len([a for a in screen.areas if is_area_valid(a)])

                        # Verify that the area was actually joined
                        if areas_after < areas_before:
                            print(f"[AniMate] Successfully merged VIEW_3D areas. Areas before: {areas_before}, after: {areas_after}")
                        else:
                            print(f"[AniMate] Area join reported success but area count didn't decrease. Areas before: {areas_before}, after: {areas_after}")
                    except Exception as e:
                        print(f"[AniMate] Area join failed in inner try block: {e}")
                else:
                    print(f"[AniMate] One or both areas are no longer valid, skipping join operation")
            except Exception as e:
                print(f"[AniMate] Failed to merge VIEW_3D areas: {e}")

    # Log the number of areas after merging
    view3d_areas_after = [area for area in screen.areas if area.type == 'VIEW_3D' and is_area_valid(area)]
    print(f"[AniMate] After merging: {len(view3d_areas_after)} VIEW_3D areas, {len(screen.areas)} total areas")

def close_image_editor():
    """
    Close the image editor preview while preserving the original layout.
    This should be called when motion capture is stopped.
    """
    try:
        window = bpy.context.window
        screen = window.screen

        # Log the initial state of areas
        total_areas_before = len(screen.areas)
        print(f"[AniMate] Initial state: {total_areas_before} total areas")

        # Count areas by type
        area_types = {}
        for area in screen.areas:
            if is_area_valid(area):
                if area.type not in area_types:
                    area_types[area.type] = 0
                area_types[area.type] += 1

        print(f"[AniMate] Areas by type: {area_types}")

        # Find the IMAGE_EDITOR area (ensure they are valid)
        image_editor_areas = [area for area in screen.areas if area.type == 'IMAGE_EDITOR' and is_area_valid(area)]
        print(f"[AniMate] Found {len(image_editor_areas)} IMAGE_EDITOR areas")

        if not image_editor_areas:
            print("[AniMate] No image editor found to close.")
            return

        # Find a VIEW_3D area to merge with (ensure they are valid)
        view3d_areas = [area for area in screen.areas if area.type == 'VIEW_3D' and is_area_valid(area)]
        print(f"[AniMate] Found {len(view3d_areas)} VIEW_3D areas")

        if not view3d_areas:
            # If no VIEW_3D area exists, convert the image editor to VIEW_3D
            for area in image_editor_areas:
                try:
                    print(f"[AniMate] Converting IMAGE_EDITOR area {area} to VIEW_3D")
                    area.type = 'VIEW_3D'
                    print(f"[AniMate] Successfully converted area {area} to VIEW_3D")
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
        print(f"[AniMate] Updated VIEW_3D areas count: {len(view3d_areas)}")

        # If there are no VIEW_3D areas, we can't continue with joining
        if not view3d_areas:
            print("[AniMate] No VIEW_3D areas found after conversion, can't continue with joining.")
            return

        # Get the largest VIEW_3D area
        main_area = max(view3d_areas, key=lambda a: a.width * a.height)
        print(f"[AniMate] Main VIEW_3D area for joining: {main_area}, size: {main_area.width}x{main_area.height}")

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
                    print(f"[AniMate] Attempting to join {area} with main area {main_area}")
                    try:
                        # Calculate the cursor position for joining
                        cursor_pos = calculate_join_cursor_position(area, main_area)
                        print(f"[AniMate] Joining image editor with 3D view at cursor position {cursor_pos}")

                        # Count areas before joining
                        areas_before = len([a for a in screen.areas if is_area_valid(a)])

                        # Use C-style override context
                        with bpy.context.temp_override(window=window, screen=screen, area=area):
                            # Set the mouse cursor position
                            bpy.context.window.cursor_warp(cursor_pos[0], cursor_pos[1])
                            # Join the areas
                            bpy.ops.screen.area_join()

                        # Count areas after joining
                        areas_after = len([a for a in screen.areas if is_area_valid(a)])

                        # Verify that the area was actually joined
                        if areas_after < areas_before:
                            print(f"[AniMate] Successfully joined image editor with 3D view. Areas before: {areas_before}, after: {areas_after}")
                        else:
                            print(f"[AniMate] Area join reported success but area count didn't decrease. Areas before: {areas_before}, after: {areas_after}")
                            # If joining didn't decrease the area count, convert to VIEW_3D
                            print(f"[AniMate] Converting area {area} to VIEW_3D as fallback")
                            area.type = 'VIEW_3D'
                    except Exception as e:
                        print(f"[AniMate] Area join failed in inner try block: {e}")
                        # If joining fails, convert to VIEW_3D
                        print(f"[AniMate] Converting area {area} to VIEW_3D after join failure")
                        area.type = 'VIEW_3D'
                else:
                    print(f"[AniMate] One or both areas are no longer valid, skipping join operation")
                    # If the area is still valid, convert it to VIEW_3D
                    if is_area_valid(area):
                        print(f"[AniMate] Converting area {area} to VIEW_3D because main area is invalid")
                        area.type = 'VIEW_3D'
            except Exception as e:
                try:
                    # If joining fails, just convert to VIEW_3D if the area is still valid
                    if is_area_valid(area):
                        print(f"[AniMate] Area join failed: {e}, converting {area} to VIEW_3D")
                        area.type = 'VIEW_3D'

                        # After converting to VIEW_3D, we need to merge it with other VIEW_3D areas
                        # This is crucial to avoid ending up with multiple VIEW_3D areas
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

            print(f"[AniMate] Final check: found {len(view3d_areas)} VIEW_3D areas")

            if len(view3d_areas) > 1:
                print(f"[AniMate] Found {len(view3d_areas)} VIEW_3D areas, merging them...")
                merge_view3d_areas(window, screen, view3d_areas)
            else:
                print(f"[AniMate] Only found {len(view3d_areas)} VIEW_3D area, no merging needed.")

            # Log the final state of areas
            total_areas_after = len(screen.areas)
            print(f"[AniMate] Final state: {total_areas_after} total areas (started with {total_areas_before})")

            # Count areas by type
            area_types = {}
            for area in screen.areas:
                if is_area_valid(area):
                    if area.type not in area_types:
                        area_types[area.type] = 0
                    area_types[area.type] += 1

            print(f"[AniMate] Final areas by type: {area_types}")
        except Exception as e:
            print(f"[AniMate] Failed to merge VIEW_3D areas: {e}")

        print("[AniMate] Preview window closed while preserving original layout.")
    except Exception as e:
        print(f"[AniMate] Error in close_image_editor: {e}")

def restore_single_3d_view():
    """
    Merge all VIEW_3D and IMAGE_EDITOR areas into a single large 3D View area, leaving other area types untouched.
    """
    try:
        window = bpy.context.window
        screen = window.screen

        # Log the initial state of areas
        total_areas_before = len(screen.areas)
        print(f"[AniMate] restore_single_3d_view: Initial state: {total_areas_before} total areas")

        # Count areas by type
        area_types = {}
        for area in screen.areas:
            if is_area_valid(area):
                if area.type not in area_types:
                    area_types[area.type] = 0
                area_types[area.type] += 1

        print(f"[AniMate] restore_single_3d_view: Areas by type: {area_types}")

        # Convert all IMAGE_EDITOR areas to VIEW_3D
        image_editor_areas = [area for area in screen.areas if area.type == 'IMAGE_EDITOR' and is_area_valid(area)]
        print(f"[AniMate] restore_single_3d_view: Found {len(image_editor_areas)} IMAGE_EDITOR areas to convert")

        for area in image_editor_areas:
            try:
                print(f"[AniMate] restore_single_3d_view: Converting IMAGE_EDITOR area {area} to VIEW_3D")
                area.type = 'VIEW_3D'
                print(f"[AniMate] restore_single_3d_view: Successfully converted area {area} to VIEW_3D")
            except Exception as e:
                print(f"[AniMate] restore_single_3d_view: Failed to convert IMAGE_EDITOR to VIEW_3D: {e}")

        # Merge all VIEW_3D areas into the largest one
        view3d_areas = [area for area in screen.areas if area.type == 'VIEW_3D' and is_area_valid(area)]
        print(f"[AniMate] restore_single_3d_view: Found {len(view3d_areas)} VIEW_3D areas to merge")

        if len(view3d_areas) > 1:
            print(f"[AniMate] restore_single_3d_view: Merging {len(view3d_areas)} VIEW_3D areas...")

            # Try a more direct approach to merge areas if there are exactly 2 VIEW_3D areas
            if len(view3d_areas) == 2:
                try:
                    area1, area2 = view3d_areas
                    print(f"[AniMate] restore_single_3d_view: Direct merge of {area1} and {area2}")

                    # Count areas before joining
                    areas_before = len([a for a in screen.areas if is_area_valid(a)])

                    # Calculate the cursor position for joining
                    cursor_pos = calculate_join_cursor_position(area1, area2)
                    print(f"[AniMate] restore_single_3d_view: Joining VIEW_3D areas with cursor at {cursor_pos}")

                    # Use C-style override context
                    with bpy.context.temp_override(window=window, screen=screen, area=area1):
                        # Set the mouse cursor position
                        bpy.context.window.cursor_warp(cursor_pos[0], cursor_pos[1])
                        # Join the areas
                        bpy.ops.screen.area_join()

                    # Count areas after joining
                    areas_after = len([a for a in screen.areas if is_area_valid(a)])

                    # Verify that the area was actually joined
                    if areas_after < areas_before:
                        print(f"[AniMate] restore_single_3d_view: Successfully merged VIEW_3D areas directly. Areas before: {areas_before}, after: {areas_after}")
                    else:
                        print(f"[AniMate] restore_single_3d_view: Direct area join didn't decrease area count. Areas before: {areas_before}, after: {areas_after}")
                        # Fall back to the standard merge approach
                        merge_view3d_areas(window, screen, view3d_areas)
                except Exception as e:
                    print(f"[AniMate] restore_single_3d_view: Direct merge failed: {e}, falling back to standard merge")
                    merge_view3d_areas(window, screen, view3d_areas)
            else:
                # Use the standard merge approach for more than 2 areas
                merge_view3d_areas(window, screen, view3d_areas)
        else:
            print(f"[AniMate] restore_single_3d_view: Only found {len(view3d_areas)} VIEW_3D area, no merging needed.")

        # Force a full UI redraw
        try:
            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
            print("[AniMate] restore_single_3d_view: Forced full UI redraw after area merge.")
        except Exception as e:
            print(f"[AniMate] restore_single_3d_view: Failed to force UI redraw: {e}")

        # Log the final state of areas
        view3d_areas_after = [area for area in screen.areas if area.type == 'VIEW_3D' and is_area_valid(area)]
        total_areas_after = len(screen.areas)
        print(f"[AniMate] restore_single_3d_view: Final state: {total_areas_after} total areas (started with {total_areas_before})")
        print(f"[AniMate] restore_single_3d_view: Final VIEW_3D areas: {len(view3d_areas_after)}")

        # Count areas by type
        area_types = {}
        for area in screen.areas:
            if is_area_valid(area):
                if area.type not in area_types:
                    area_types[area.type] = 0
                area_types[area.type] += 1

        print(f"[AniMate] restore_single_3d_view: Final areas by type: {area_types}")

        print("[AniMate] Restored single 3D View area (leaving other area types untouched).")
    except Exception as e:
        print(f"[AniMate] Error in restore_single_3d_view: {e}")

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
