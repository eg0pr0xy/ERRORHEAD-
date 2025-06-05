# GUI Preview Mode

import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import cv2
import os
import threading
import time

from core.shader_manager import ShaderManager
from core.glitch_frame_wild import glitch_frame_wild

class GlitchGuiPreview:
    def __init__(self, master):
        self.master = master
        self.input_path = None
        # self.shader_manager will be created and managed within the _preview_loop thread
        self.video_width = 0
        self.video_height = 0
        self.cap = None
        self.playing = False
        self.preview_thread = None
        self.current_frame_pil = None
        self.preview_width = 640
        self.preview_height = 360

        # Get available shaders
        self.shader_dir = os.path.join(os.path.dirname(__file__), '..', 'shaders')
        self.available_shaders = [f for f in os.listdir(self.shader_dir) if f.endswith('.glsl')]
        if not self.available_shaders:
            self.available_shaders = ["No shaders found"]
        self.selected_shader_path = tk.StringVar(value=self.available_shaders[0])

        self.build_ui()

    def build_ui(self):
        # --- Top Controls Frame ---
        controls_frame = ttk.Frame(self.master, padding=10)
        controls_frame.pack(fill=tk.X)

        # Load Video Button
        ttk.Button(controls_frame, text="🎞️ Video laden", command=self.load_video).pack(side=tk.LEFT, padx=5)
        self.video_label = ttk.Label(controls_frame, text="Kein Video geladen")
        self.video_label.pack(side=tk.LEFT, padx=5)

        # --- Preview Area ---
        self.preview_label = ttk.Label(self.master)
        self.preview_label.pack(pady=10, expand=True, fill=tk.BOTH)
        # Placeholder image
        placeholder_img = Image.new("RGB", (self.preview_width, self.preview_height), "black")
        self.update_preview_image(placeholder_img)

        # --- Bottom Controls Frame ---
        bottom_controls_frame = ttk.Frame(self.master, padding=10)
        bottom_controls_frame.pack(fill=tk.X)

        # Shader Selection
        ttk.Label(bottom_controls_frame, text="Shader:").pack(side=tk.LEFT, padx=(0,5))
        shader_menu = ttk.OptionMenu(bottom_controls_frame, self.selected_shader_path, self.available_shaders[0], *self.available_shaders, command=self.on_shader_select)
        shader_menu.pack(side=tk.LEFT, padx=5)

        # Intensity Slider
        self.vid_intensity = tk.DoubleVar(value=0.5)
        ttk.Label(bottom_controls_frame, text="Intensität:").pack(side=tk.LEFT, padx=(10,0))
        ttk.Scale(bottom_controls_frame, from_=0, to=1,
                  orient="horizontal", variable=self.vid_intensity, length=150).pack(side=tk.LEFT, padx=5)

        # Play/Pause/Stop Buttons
        self.play_button = ttk.Button(bottom_controls_frame, text="▶ Play", command=self.toggle_play_pause, state=tk.DISABLED)
        self.play_button.pack(side=tk.LEFT, padx=5)
        self.stop_button = ttk.Button(bottom_controls_frame, text="⏹ Stop", command=self.stop_preview, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

    def update_preview_image(self, pil_image):
        try:
            imgtk = ImageTk.PhotoImage(image=pil_image)
            self.preview_label.imgtk = imgtk # Keep a reference
            self.preview_label.config(image=imgtk)
        except Exception as e:
            print(f"Error updating preview image: {e}")

    def load_video(self):
        path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mov *.avi")])
        if path:
            self.input_path = path
            self.video_label.config(text=os.path.basename(path))
            self.play_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            if self.playing:
                self.stop_preview() # Stop if already playing another video
            self.prepare_video_capture()

    def prepare_video_capture(self):
        if self.input_path:
            self.cap = cv2.VideoCapture(self.input_path)
            if not self.cap.isOpened():
                print(f"Error: Could not open video {self.input_path}")
                self.cap = None
                return
            # Get video properties for ShaderManager (if needed later)
            # width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            # height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.video_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.video_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            # ShaderManager will be initialized in _preview_loop
            # Display first frame as static preview
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.current_frame_pil = Image.fromarray(frame_rgb).resize((self.preview_width, self.preview_height), Image.LANCZOS)
                self.update_preview_image(self.current_frame_pil)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # Reset to beginning

    def on_shader_select(self, selected_shader_name):
        # This callback is triggered when a shader is selected from the OptionMenu
        # self.selected_shader_path.set(selected_shader_name) # Variable is already updated
        # If live preview is running and shader changes, it should pick up the new shader
        # Or, we might need to restart the preview thread or update it if shader_manager is robust to shader changes
        print(f"Selected shader: {self.selected_shader_path.get()}")

    def toggle_play_pause(self):
        if not self.cap:
            return
        if self.playing:
            self.playing = False
            self.play_button.config(text="▶ Play")
            # The thread will see self.playing is False and exit its loop
        else:
            self.playing = True
            self.play_button.config(text="⏸ Pause")
            if self.preview_thread is None or not self.preview_thread.is_alive():
                self.preview_thread = threading.Thread(target=self._preview_loop, daemon=True)
                self.preview_thread.start()

    def stop_preview(self):
        self.playing = False
        if self.preview_thread and self.preview_thread.is_alive():
            self.preview_thread.join(timeout=0.5) # Wait briefly for thread to stop
        self.preview_thread = None
        if self.cap:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # Reset video to beginning
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.current_frame_pil = Image.fromarray(frame_rgb).resize((self.preview_width, self.preview_height), Image.LANCZOS)
                self.update_preview_image(self.current_frame_pil)
        self.play_button.config(text=" Play")

    def _preview_loop(self):
        if not self.cap or self.video_width == 0 or self.video_height == 0:
            self.playing = False # Ensure playing is false if prerequisites not met
            self.master.after(0, lambda: self.play_button.config(text="▶ Play"))
            return

        local_shader_manager = None
        try:
            local_shader_manager = ShaderManager(width=self.video_width, height=self.video_height)
            print("ShaderManager initialized for preview thread.")
        except Exception as e:
            print(f"Failed to initialize ShaderManager in preview thread: {e}. Shader effects will be disabled.")
            local_shader_manager = None

        fps = self.cap.get(cv2.CAP_PROP_FPS)
        if fps == 0: fps = 30 # Default if FPS not readable
        delay_ms = int(1000 / fps)

        while self.playing and self.cap.isOpened():
            ret, frame_bgr = self.cap.read()
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # Loop video
                ret, frame_bgr = self.cap.read()
                if not ret: break # Break if loop also fails

            if local_shader_manager and self.selected_shader_path.get() != "No shaders found":
                shader_full_path = os.path.join(self.shader_dir, self.selected_shader_path.get())
                if os.path.exists(shader_full_path):
                    effective_audio_amp = self.vid_intensity.get()
                    processed_frame_rgb = glitch_frame_wild(frame_bgr,
                                                            local_shader_manager,
                                                            shader_full_path,
                                                            self.vid_intensity.get(),
                                                            effective_audio_amp)
                    self.current_frame_pil = Image.fromarray(processed_frame_rgb).resize((self.preview_width, self.preview_height), Image.LANCZOS)
                else:
                    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
                    self.current_frame_pil = Image.fromarray(frame_rgb).resize((self.preview_width, self.preview_height), Image.LANCZOS)
            else:
                frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
                self.current_frame_pil = Image.fromarray(frame_rgb).resize((self.preview_width, self.preview_height), Image.LANCZOS)
            
            # Schedule GUI update on the main thread
            self.master.after(0, self.update_preview_image, self.current_frame_pil)
            
            time.sleep(delay_ms / 1000.0)

        # Clean up when loop ends
        if local_shader_manager and hasattr(local_shader_manager, 'ctx') and local_shader_manager.ctx:
            try:
                local_shader_manager.ctx.release()
                print("ShaderManager context released from preview thread.")
            except Exception as e:
                print(f"Error releasing ShaderManager context in preview thread: {e}")
        local_shader_manager = None

        self.playing = False
        # Ensure button text is correct if loop ends naturally or due to error
        self.master.after(0, lambda: self.play_button.config(text="▶ Play"))

    def on_close(self):
        """Called when the main window is closing or tab is switched."""
        self.stop_preview()
        if self.cap:
            self.cap.release()
        # ShaderManager is now managed by the _preview_loop thread.
        # stop_preview ensures the thread finishes, which handles its own SM release.
        print("GlitchGuiPreview closed.")

# Example of how to integrate into main.py (for testing this file standalone)
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Preview Test")
    root.geometry("700x550")
    # from ttkbootstrap import Style
    # style = Style(theme='darkly') # Optional: use ttkbootstrap style
    preview_tab = ttk.Frame(root)
    preview_tab.pack(fill="both", expand=True)
    app = GlitchGuiPreview(preview_tab)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.on_close(), root.destroy()))
    root.mainloop()