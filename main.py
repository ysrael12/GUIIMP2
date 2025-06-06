import tkinter as tk
from WinMainTk import WinMainTk

if __name__ == "__main__":
    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.title("GUIMIMP - Medical Imaging")
    root.minsize(800, 600)
    
    app = WinMainTk(root)
    app.mainloop()