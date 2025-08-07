from abc import ABC, abstractmethod
import customtkinter as tk
import tkinter as tkinter

class UtilObject(ABC):
    @abstractmethod
    def getMainGUI(self, parent:tk.Tk) -> tkinter.Frame:
        pass