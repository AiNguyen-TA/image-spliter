import customtkinter as tk
from utilObject import UtilObject

class util1(UtilObject):
    def __init__(self, frameObject: tk.CTkFrame):
        self.root = frameObject
        self.root.configure(fg_color='#f4ae01')
