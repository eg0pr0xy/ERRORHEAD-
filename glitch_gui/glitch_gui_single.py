# glitch_gui/glitch_gui_single.py

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from ttkbootstrap import Style
from core import glitch_sync
import os

class GlitchGuiSingle:
    def __init__(self, master):
        self.master = master
        self.master.title("ERRORHEAD - Single Glitch")
        self.master.geometry("800x600")
        self.style = Style("darkly")

        self.input_path = None
        self.audio_path = None

        self.build_ui()

    def build_ui(self):
        self.title_label = tk.Label(self.master, text="ERRORHEAD", font=("Consolas", 20, "bold"), fg="white", bg="black")
        self.title_label.pack(pady=10)

        # Background logo
        bg_img = Image.open("assets/logo_errorhead.png").resize((600, 600)).convert("RGBA")
        bg_img.putalpha(64)
        self.bg_image = ImageTk.PhotoImage(bg_img)
        self.bg_canvas = tk.Canvas(self.master, width=600, height=600, highlightthickness=0, bg="black")
        self.bg_canvas.place(relx=0.5, rely=0.5, anchor="center")
        self.bg_canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        self.bg_canvas.lower()

        # Load video
        tk.Button(self.master, text="🎞️ Video laden", command=self.load_video).pack(pady=5)
        self.video_label = tk.Label(self.master, text="Kein Video geladen", fg="gray", bg="black")
        self.video_label.pack()

        # Load audio
        tk.Button(self.master, text="🎵 Audio laden", command=self.load_audio).pack(pady=5)
        self.audio_label = tk.Label(self.master, text="Kein Audio geladen", fg="gray", bg="black")
        self.audio_label.pack()

        # Intensity sliders
        self.vid_intensity = tk.DoubleVar(value=0.5)
        tk.Scale(self.master, label="Video-Intensität", from_=0, to=1, resolution=0.01,
                 orient="horizontal", variable=self.vid_intensity).pack(pady=5)

        self.aud_intensity = tk.DoubleVar(value=0.5)
        tk.Scale(self.master, label="Audio-Intensität", from_=0, to=1, resolution=0.01,
                 orient="horizontal", variable=self.aud_intensity).pack(pady=5)

        # Export button
        tk.Button(self.master, text="💥 GLITCH EXPORT", command=self.export).pack(pady=10)

    def load_video(self):
        path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mov *.avi")])
        if path:
            self.input_path = path
            self.video_label.config(text=os.path.basename(path), fg="white")

    def load_audio(self):
        path = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav *.mp3")])
        if path:
            self.audio_path = path
            self.audio_label.config(text=os.path.basename(path), fg="white")

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