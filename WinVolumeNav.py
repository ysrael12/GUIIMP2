import tkinter as tk
from tkinter import ttk

class WinVolumeNav(tk.Frame):
    def __init__(self, parent, main_app):
        super().__init__(parent)
        self.main_app = main_app
        self.updating_slider = False  # Flag para evitar loop de recursão
        self.create_widgets()
        self.configure_layout()

    def create_widgets(self):
        self.slider = ttk.Scale(
            self,
            from_=0,
            to=0,
            orient=tk.HORIZONTAL,
            command=self.update_slice
        )
        self.slider.pack(fill=tk.X, padx=5, pady=5)

        self.controls_frame = ttk.Frame(self)
        self.controls_frame.pack(fill=tk.X)

        self.btn_prev = ttk.Button(
            self.controls_frame,
            text="◀",
            width=3,
            command=lambda: self.change_slice(-1)
        )
        self.btn_prev.pack(side=tk.LEFT)

        self.lbl_slice = ttk.Label(
            self.controls_frame,
            text="0/0",
            width=10,
            anchor=tk.CENTER
        )
        self.lbl_slice.pack(side=tk.LEFT, expand=True)

        self.btn_next = ttk.Button(
            self.controls_frame,
            text="▶",
            width=3,
            command=lambda: self.change_slice(1)
        )
        self.btn_next.pack(side=tk.LEFT)

        self.set_max_slices(0)

    def configure_layout(self):
        self.pack_propagate(False)
        self.config(width=200, height=80)
        self.pack(fill=tk.X, padx=5, pady=5)

    def set_max_slices(self, max_slices):
        self.max_slices = max_slices
        self.slider.config(to=max_slices - 1 if max_slices > 0 else 0)
        self.update_slice(0)

    def update_slice(self, value):
        if self.updating_slider:
            return
        try:
            slice_idx = int(float(value))
            slice_idx = max(0, min(slice_idx, self.max_slices - 1))
            self.lbl_slice.config(text=f"{slice_idx + 1}/{self.max_slices}")
            self.main_app.show_slice(slice_idx)
        except (ValueError, TypeError):
            pass

    def change_slice(self, delta):
        current = int(float(self.slider.get()))
        new_slice = max(0, min(current + delta, self.max_slices - 1))
        self.slider.set(new_slice)
        self.update_slice(new_slice)

    def update_from_external(self, slice_idx):
        if int(float(self.slider.get())) != int(slice_idx):
            self.updating_slider = True
            self.slider.set(slice_idx)
            self.updating_slider = False
        self.lbl_slice.config(text=f"{slice_idx + 1}/{self.max_slices}")
