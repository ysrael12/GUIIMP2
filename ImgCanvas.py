import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

class ImgCanvas(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, bg='black', highlightthickness=0)
        self.image = None
        self.photo_image = None
        self.bind("<Configure>", self.resize)

    def set_image(self, image_array):
        self.image = image_array
        self.draw_image()

    def draw_image(self):
        if self.image is not None:
            img = Image.fromarray(self.image)
            self.photo_image = ImageTk.PhotoImage(img)
            self.create_image(0, 0, image=self.photo_image, anchor=tk.NW)

    def resize(self, event):
        if self.image is not None:
            self.draw_image()