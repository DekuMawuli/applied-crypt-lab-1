import tkinter as tk

from ui import App

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    # On macOS a Tk window started from a terminal can open behind other windows
    root.lift()
    root.attributes("-topmost", True)
    root.after(200, lambda: root.attributes("-topmost", False))
    root.focus_force()
    root.mainloop()
