# glitch_gui/glitch_gui_single.py

import tkinter as tk
from tkinter import ttk # Import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
# from ttkbootstrap import Style # Style is managed globally
from core import glitch_sync
import os

class GlitchGuiSingle:
    def __init__(self, master):
        self.master = master
        # self.style = Style("darkly") # Style should be applied to root or not at all here to avoid conflicts

        self.input_path = None
        self.audio_path = None

        self.build_ui()

    def build_ui(self):
        self.title_label = ttk.Label(self.master, text="ERRORHEAD", font=("Consolas", 20, "bold")) # Removed fg, bg
        self.title_label.pack(pady=10)

        # Background logo
        bg_img = Image.open("assets/logo_errorhead.png").resize((600, 600)).convert("RGBA")
        bg_img.putalpha(64)
        self.bg_image = ImageTk.PhotoImage(bg_img)
        self.bg_canvas = tk.Canvas(self.master, width=600, height=600, highlightthickness=0) # Removed bg="black"
        self.bg_canvas.place(relx=0.5, rely=0.5, anchor="center")
        self.bg_canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        # self.bg_canvas.lower() # Removed call to lower()

        # Load video
        ttk.Button(self.master, text="🎞️ Video laden", command=self.load_video).pack(pady=5)
        self.video_label = ttk.Label(self.master, text="Kein Video geladen") # Removed fg, bg
        self.video_label.pack()

        # Load audio
        ttk.Button(self.master, text="🎵 Audio laden", command=self.load_audio).pack(pady=5)
        self.audio_label = ttk.Label(self.master, text="Kein Audio geladen") # Removed fg, bg
        self.audio_label.pack()

        # Intensity sliders
        self.vid_intensity = tk.DoubleVar(value=0.5)
        ttk.Label(self.master, text="Video-Intensität").pack(pady=(10,0))
        ttk.Scale(self.master, from_=0, to=1,
                  orient="horizontal", variable=self.vid_intensity, length=200).pack(pady=5, fill=tk.X, padx=50)

        self.aud_intensity = tk.DoubleVar(value=0.5)
        ttk.Label(self.master, text="Audio-Intensität").pack(pady=(10,0))
        ttk.Scale(self.master, from_=0, to=1,
                  orient="horizontal", variable=self.aud_intensity, length=200).pack(pady=5, fill=tk.X, padx=50)

        # Export button
        ttk.Button(self.master, text="💥 GLITCH EXPORT", command=self.export).pack(pady=20)

    def load_video(self):
        path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mov *.avi")])
        if path:
            self.input_path = path
            self.video_label.config(text=os.path.basename(path)) # Removed fg

    def load_audio(self):
        path = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav *.mp3")])
        if path:
            self.audio_path = path
            self.audio_label.config(text=os.path.basename(path)) # Removed fg

    def export(self):
        if not self.input_path:
            print("Kein Video geladen.")
            return
        output_path = filedialog.asksaveasfilename(defaultextension=".mp4")
        if not output_path:
            return
        glitch_sync.glitch_sync(
            input_video=self.input_path,
            output_video=output_path,
            vid_intensity=self.vid_intensity.get(),
            aud_intensity=self.aud_intensity.get(),
            audio_mode="bitcrush",
            external_audio_path=self.audio_path
        )