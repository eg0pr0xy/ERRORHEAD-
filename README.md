# <img src="assets/logo_errorhead.png" alt="ERRORHEAD Logo" width="50"/> ERRORHEAD - Video Glitch Tool

ERRORHEAD is a Python-based desktop application for creating unique glitch art from your videos. It combines audio-reactive elements with shader-based visual effects to offer a range of creative possibilities.

## Features

*   **Single Glitch Mode:**
    *   Load video files (MP4, MOV, AVI).
    *   Optionally load an external audio file (WAV, MP3) to drive effects or replace original audio.
    *   Adjustable video glitch intensity.
    *   Adjustable audio glitch intensity (currently bitcrushing).
    *   Audio-reactive video effects using GLSL shaders (e.g., `reactive_wave.glsl`).
    *   Export glitched videos in MP4 format.
*   **User-Friendly Interface:** Built with Tkinter and `ttkbootstrap` for a modern look and feel.

**Planned Features:**
*   Live Preview Mode.
*   Batch Processing Mode.
*   More diverse audio glitch effects.
*   A wider selection of GLSL shaders and easier shader management through the GUI.
*   More granular control over glitch parameters.

## Requirements

*   Python 3.7+
*   FFmpeg (must be installed and accessible in your system's PATH for `moviepy` to work correctly for video export).
*   Dependencies listed in `requirements.txt`:
    *   `numpy`
    *   `opencv-python`
    *   `pydub`
    *   `scipy`
    *   `Pillow`
    *   `moviepy`
    *   `ttkbootstrap`
    *   `moderngl` (implicitly required by `shader_manager`)

## Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd ERRORHEAD
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: Ensure you have FFmpeg installed and in your PATH. Visit [ffmpeg.org](https://ffmpeg.org/download.html) for installation instructions.*

4.  **Run the application:**
    ```bash
    python main.py
    ```

5.  **Using the Tool (Single Glitch Tab):**
    *   Click "🎞️ Video laden" to select your input video.
    *   (Optional) Click "🎵 Audio laden" to select an external audio file. If not selected, the original video's audio will be used.
    *   Adjust the "Video-Intensität" and "Audio-Intensität" sliders.
    *   Click "💥 GLITCH EXPORT" and choose a save location and filename for your glitched video.

## Contributing

Contributions are welcome! If you'd like to contribute, please:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes.
4.  Submit a pull request with a clear description of your changes.

## License

This project is currently unlicensed. You are free to use, modify, and distribute it, but please provide attribution if you share it publicly. Consider adding an open-source license like MIT if you plan for wider collaboration.

---

*Glitch art with ERRORHEAD!*
