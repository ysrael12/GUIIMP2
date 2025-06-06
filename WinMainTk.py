import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import os
import my
from PIL import Image, ImageTk
import ImgCanvas as ic
import WinWindowLevel
from WinVolumeNav import WinVolumeNav

class WinMainTk(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.volume = None
        self.current_slice = 0
        self.create_widgets()
        self.bind_events()

    def create_widgets(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Canvas principal
        self.canvas = ic.ImgCanvas(self.root)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        
        # Painel de controle lateral
        self.toolbox = ttk.Frame(self.root, width=250)
        self.toolbox.grid(row=0, column=1, sticky='nsew')
        
        # Controle de slices
        self.volume_nav = WinVolumeNav(self.toolbox, self)
        
        # Botões de controle
        self.window_level_btn = ttk.Button(
            self.toolbox, 
            text="Window/Level",
            command=self.open_window_level
        )
        self.window_level_btn.pack(pady=5)
        
        # Menu principal
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open DICOM", command=self.open_dicom)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    def bind_events(self):
        self.root.bind("<Left>", lambda e: self.change_slice(-1))
        self.root.bind("<Right>", lambda e: self.change_slice(1))

    def open_dicom(self):
        file_path = filedialog.askopenfilename(filetypes=[("Medical Images", "*.mhd")])
        if file_path:
            try:
                seriesuid = os.path.basename(file_path).split('.')[0]
                self.load_volume(seriesuid)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def load_volume(self, seriesuid):
        ct_data = my.load_ct_scan(seriesuid)
        self.volume = my.normalize_hu(ct_data['image'])
        self.volume_nav.set_max_slices(self.volume.shape[0])
        self.show_slice(0)

    def show_slice(self, slice_idx):
        if self.volume is not None:
            self.current_slice = np.clip(slice_idx, 0, self.volume.shape[0]-1)
            slice_img = self.volume[self.current_slice]
            self.canvas.set_image(slice_img)
            self.volume_nav.update_from_external(self.current_slice)

    def change_slice(self, delta):
        self.show_slice(self.current_slice + delta)

    def open_window_level(self):
        if self.volume is not None:
            WinWindowLevel.WinWindowLevel(self.root, self)