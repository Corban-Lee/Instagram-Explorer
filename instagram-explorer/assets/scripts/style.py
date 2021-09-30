from tkinter import ttk


class Style(ttk.Style):
    def __init__(self, master):
        super().__init__(master)
        
        self.configure(".", font=("HP Simplified Jpan Light", 15))
        self.configure("TLabel", font=("HP Simplified Jpan Light", 15), anchor="center")
        
        self.configure("RootBody.TFrame", background="#FAF9F6")
        
        self.configure("Titlebar.TLabel", anchor="center")
        self.configure("TitlebarButton.TLabel", anchor="center")
        self.map("TitlebarButton.TLabel", background=[("pressed", "#E0E0E0"), ("active", "#EEEEEE")])
        
        
        self.configure("SidebarButton.TLabel", anchor="w", font=("HP Simplified Jpan Light", 15))
        self.map("SidebarButton.TLabel", background=[("pressed", "#E0E0E0"), ("active", "#EEEEEE")])