# main.py – ERRORHEAD Launcher

import tkinter as tk
from tkinter import ttk # Import ttk
from ttkbootstrap import Style, Notebook
from glitch_gui.glitch_gui_single import GlitchGuiSingle
from glitch_gui.glitch_gui_preview import GlitchGuiPreview

def main():
    root = tk.Tk()
    root.title("ERRORHEAD – Video Glitch Tool")
    root.geometry("900x700")
    style = Style("darkly")

    notebook = Notebook(root, bootstyle="dark")
    notebook.pack(fill="both", expand=True)

    # Tab 1 – Single Glitch
    tab_single = ttk.Frame(notebook) # Use ttk.Frame
    notebook.add(tab_single, text="🎞️ Single Glitch")
    GlitchGuiSingle(tab_single)

    # Tab 2 - Live Preview
    tab_preview_frame = ttk.Frame(notebook) # Use ttk.Frame
    notebook.add(tab_preview_frame, text="👁️ Live Preview")
    glitch_gui_preview_instance = GlitchGuiPreview(tab_preview_frame)

    tab_batch = ttk.Frame(notebook) # Use ttk.Frame
    notebook.add(tab_batch, text="🗂️ Batch Mode (Coming Soon)")

    # Placeholder content for Batch Mode
    lbl_batch = ttk.Label(tab_batch, text="Batch processing features will be here.", font=("Consolas", 12))
    lbl_batch.pack(padx=20, pady=20)

    def on_app_close():
        # Call on_close for all relevant GUI components
        if 'glitch_gui_preview_instance' in locals() and hasattr(glitch_gui_preview_instance, 'on_close'):
            glitch_gui_preview_instance.on_close()
        # Add similar calls for other tabs if they have cleanup routines
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_app_close)
    root.mainloop()

if __name__ == "__main__":
    main()