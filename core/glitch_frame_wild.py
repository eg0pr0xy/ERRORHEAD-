# core/glitch_frame_wild.py

import numpy as np
import os # Ensure os is imported

# ShaderManager will be passed as an argument

def glitch_frame_wild(frame_np, shader_manager, shader_path, vid_intensity, audio_amplitude):
    """
    Applies a shader to the video frame.

    Args:
        frame_np (np.array): The input video frame as a NumPy array (BGR format from OpenCV).
        shader_manager (ShaderManager): Instance of the ShaderManager.
        shader_path (str): Path to the GLSL fragment shader file.
        vid_intensity (float): General intensity for the video glitch (0.0 to 1.0).
        audio_amplitude (float): Amplitude derived from audio (0.0 to 1.0), for reactive effects.

    Returns:
        np.array: The glitched video frame as a NumPy array (RGB format for MoviePy).
    """
    # Always convert BGR to RGB first, as this will be the expected output format
    frame_rgb = frame_np[:, :, ::-1].copy() # Convert BGR to RGB

    if shader_manager is None or shader_path is None:
        # Fallback if shader system isn't ready, return the RGB-converted original frame
        # Or, implement a basic numpy-based glitch here on frame_rgb as an alternative
        return frame_rgb

    # Define uniforms based on the shader
    shader_name = os.path.basename(shader_path)
    uniforms = {}

    if shader_name == "reactive_wave.glsl":
        uniforms["amplitude"] = audio_amplitude * vid_intensity # Combine audio reactivity
    elif shader_name == "rgb_split.glsl":
        # Scale vid_intensity for a reasonable offset range (e.g., 0.0 to 0.05)
        uniforms["offset_amount"] = vid_intensity * 0.05 
    else:
        # Default uniform for other shaders, or can be left empty
        uniforms["intensity"] = vid_intensity

    try:
        glitched_frame_rgb = shader_manager.apply_shader(frame_rgb, shader_path, uniforms)
        # shader_manager.apply_shader returns RGB, which is what FFMPEG_VideoWriter in glitch_sync expects
        return glitched_frame_rgb
    except Exception as e:
        print(f"Error applying shader {shader_path}: {e}")
        # Fallback to the RGB-converted original frame in case of shader error
        return frame_rgb