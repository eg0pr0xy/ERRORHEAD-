# core/glitch_sync.py

import cv2
import numpy as np
import os
from moviepy.editor import VideoFileClip, AudioFileClip
from core.glitch_frame_wild import glitch_frame_wild
from core.audio_input import AudioReactiveInput
from core.audio_trigger_map import extract_trigger_times
from moviepy.video.io.ffmpeg_writer import FFMPEG_VideoWriter
from core.shader_manager import ShaderManager

def extract_audio(input_video, output_audio):
    video = VideoFileClip(input_video)
    video.audio.write_audiofile(output_audio)

def glitch_audio_with_mode(input_audio, output_audio, mode="bitcrush", intensity=0.5):
    from pydub import AudioSegment

    audio = AudioSegment.from_file(input_audio)

    if mode == "bitcrush":
        # Reduce sample width (bit depth)
        # Original is typically 2 bytes (16-bit). We'll reduce to 1 byte (8-bit) at max intensity.
        target_sample_width = 2 - int(round(intensity)) # 2 for intensity 0-0.49, 1 for 0.5-1.0
        if target_sample_width < 1: target_sample_width = 1
        if target_sample_width > audio.sample_width: target_sample_width = audio.sample_width
        
        audio = audio.set_sample_width(target_sample_width)

        # Reduce frame rate
        # Max reduction to 1/4 of original rate at full intensity
        original_frame_rate = audio.frame_rate
        target_frame_rate = int(original_frame_rate * (1 - (intensity * 0.75)))
        if target_frame_rate < 8000: # Ensure a minimum reasonable frame rate
            target_frame_rate = 8000 
        if target_frame_rate > original_frame_rate: target_frame_rate = original_frame_rate

        audio = audio.set_frame_rate(target_frame_rate)
        
        audio.export(output_audio, format="wav")
    else:
        # Fallback: Copy audio if mode is not recognized
        import shutil
        shutil.copy(input_audio, output_audio)

def glitch_sync(input_video, output_video,
                vid_intensity=0.5, aud_intensity=0.5,
                audio_mode="bitcrush", external_audio_path=None):

    # Ensure temporary files are unique enough or cleaned up if running multiple times
    # For simplicity, using fixed names here but consider tempfile module for robustness
    base_name = os.path.splitext(os.path.basename(input_video))[0]
    tmp_audio_original = f"temp_{base_name}_original_audio.wav"
    tmp_audio_glitched = f"temp_{base_name}_glitched_audio.wav"

    if external_audio_path:
        audio_path = external_audio_path
    else:
        extract_audio(input_video, tmp_audio_original)
        audio_path = tmp_audio_original

    glitch_audio_with_mode(audio_path, tmp_audio_glitched, audio_mode, aud_intensity)
    trigger_times = extract_trigger_times(audio_path)

    cap = cv2.VideoCapture(input_video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    writer = FFMPEG_VideoWriter(output_video, (w, h), fps, codec="libx264")

    # Initialize ShaderManager
    shader_manager = None
    try:
        shader_manager = ShaderManager(width=w, height=h)
    except Exception as e:
        print(f"Failed to initialize ShaderManager: {e}. Video glitching will be basic or disabled.")

    # TODO: Make shader selection dynamic (e.g., from GUI)
    # For now, hardcode to reactive_wave.glsl. Ensure path is correct.
    # Assuming shaders directory is at the same level as core, or adjust path as needed.
    shader_file_path = os.path.join(os.path.dirname(__file__), '..', 'shaders', 'reactive_wave.glsl')
    if not os.path.exists(shader_file_path):
        print(f"Shader file not found: {shader_file_path}. Shader glitching will be disabled.")
        shader_manager = None # Disable if specific shader is missing

    for i in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break

        t = i / fps
        trigger_active = any(abs(t - ts) < 0.05 for ts in trigger_times)
        amp = 0.75 if trigger_active else 0.0

        # glitch_frame_wild now always returns an RGB frame.
        # 'frame' is BGR from OpenCV.
        glitched_frame_rgb = glitch_frame_wild(frame, shader_manager, shader_file_path, vid_intensity, amplitude=amp)
        writer.write_frame(glitched_frame_rgb)  # Frame is RGB

    writer.close()
    cap.release()

    if shader_manager and hasattr(shader_manager, 'ctx') and shader_manager.ctx:
        shader_manager.ctx.release()

    # Kombiniere mit Audio
    final = VideoFileClip(output_video).set_audio(AudioFileClip(tmp_audio_glitched))
    # Overwrite the selected output_video path directly with the final version
    final.write_videofile(output_video, codec="libx264", audio_codec="aac")

    # Clean up temporary audio files
    if os.path.exists(tmp_audio_original) and not external_audio_path:
        os.remove(tmp_audio_original)
    if os.path.exists(tmp_audio_glitched):
        os.remove(tmp_audio_glitched)