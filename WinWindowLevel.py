import tkinter as tk
from tkinter import ttk
import my
import numpy as np
class WinWindowLevel(tk.Toplevel):
    def __init__(self, parent, main_app):
        super().__init__(parent)
        self.main_app = main_app
        self.title("Window/Level Adjustment")
        self.geometry("300x150")
        
        self.level = tk.DoubleVar(value=-600)
        self.width = tk.DoubleVar(value=1500)
        
        ttk.Label(self, text="Level").pack()
        ttk.Scale(self, from_=-1000, to=1000, variable=self.level,
                command=self.update_window).pack(fill=tk.X)
        
        ttk.Label(self, text="Width").pack()
        ttk.Scale(self, from_=50, to=3000, variable=self.width,
                command=self.update_window).pack(fill=tk.X)
        
        ttk.Button(self, text="Apply", command=self.apply_window).pack(pady=5)

    def update_window(self, *args):
        if self.main_app.volume is not None:
            current_slice = self.main_app.current_slice
            windowed = my.apply_window(
                self.main_app.volume[current_slice],
                self.level.get(),
                self.width.get()
            )
            self.main_app.canvas.set_image(windowed)

    def apply_window(self):
        self.main_app.volume = np.array([
            my.apply_window(slice_img, self.level.get(), self.width.get())
            for slice_img in self.main_app.volume
        ])
        self.destroy()