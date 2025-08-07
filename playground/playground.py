import customtkinter as tk
import utils1 as utils1

class UtilUI():
    def __init__(self):
        self.app = tk.CTk()
        self.app.geometry('500x500')
        self.frame1 = tk.CTkFrame(self.app)
        self.util1 = utils1.util1(self.frame1)
        self.frame1.pack(fill='both', expand=True)

        self.app.bind('<Escape>', lambda Event: self.app.quit())
        self.app.mainloop()
UtilUI()