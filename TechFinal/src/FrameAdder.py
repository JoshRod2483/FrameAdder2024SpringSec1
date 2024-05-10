# alt + shift + m
import maya.cmds as cmds

def shift_keys(shift_direction):
    selection = cmds.ls(sl=True)
    if not selection:
        cmds.warning("Please select at least one object with keyframes.")
        return
    
    # Get current time
    current_time = cmds.currentTime(query=True)
    
    for obj in selection:
        # Get keyframes for the selected object, including solid and hollow keyframes
        keyframes = cmds.keyframe(obj, query=True, controlPoints=True)
        if not keyframes:
            cmds.warning("Selected object {} has no keyframes.".format(obj))
            continue
        
        print("Before shifting keyframes for", obj, ":", keyframes)
        
        # Shift keyframes and animation
        for frame in keyframes:
            if frame == current_time:
                continue  # Skip shifting the current time
            if shift_direction == "left" and frame < current_time:
                continue  # Skip shifting keys before the current time
            elif shift_direction == "right" and frame <= current_time:
                continue  # Skip shifting keys at or before the current time
            
            # Copy animation data of the keyframe
            cmds.copyKey(obj, time=(frame, frame))
            
            # Shift the keyframe
            if shift_direction == "right":
                cmds.pasteKey(obj, time=(frame + 1,))
            elif shift_direction == "left":
                cmds.pasteKey(obj, time=(frame - 1,))
            
            # Delete the original keyframe
            cmds.cutKey(obj, time=(frame, frame))
        
        # Print keyframes after shifting
        keyframes_after = cmds.keyframe(obj, query=True, controlPoints=True)
        print("After shifting keyframes for", obj, ":", keyframes_after)
    
    # Set the current time to the original time
    cmds.currentTime(current_time)

def shift_left_callback(*args):
    shift_keys("left")

def shift_right_callback(*args):
    shift_keys("right")

def create_window():
    if cmds.window("keyShiftWindow", exists=True):
        cmds.deleteUI("keyShiftWindow", window=True)
    
    window = cmds.window("keyShiftWindow", title="Keyframe Shifter", widthHeight=(200, 100))
    cmds.columnLayout(adjustableColumn=True)
    cmds.button(label="Remove Frame", command=shift_left_callback)
    cmds.button(label="Add Frame", command=shift_right_callback)
    cmds.showWindow(window)

create_window()
