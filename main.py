# main.py – ERRORHEAD Launcher

import tkinter as tk
from ttkbootstrap import Style, Notebook
from glitch_gui.glitch_gui_single import GlitchGuiSingle

def main():
    root = tk.Tk()
    root.title("ERRORHEAD – Video Glitch Tool")
    root.geometry("900x700")
    style = Style("darkly")

    notebook = Notebook(root, bootstyle="dark")
    notebook.pack(fill="both", expand=True)

    # Tab 1 – Single Glitch
    tab_single = tk.Frame(notebook)
    notebook.add(tab_single, text="🎞️ Single Glitch")
    GlitchGuiSingle(tab_single)

    # Tabs 2 & 3 als Platzhalter
    tab_preview = tk.Frame(notebook)
    notebook.add(tab_preview, text="👁️ Live Preview (Coming Soon)")

    tab_batch = tk.Frame(notebook)
    notebook.add(tab_batch, text="🗂️ Batch Mode (Coming Soon)")

    root.mainloop()

if __name__ == "__main__":
    main()