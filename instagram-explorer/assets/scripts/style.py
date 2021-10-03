from tkinter import ttk

import assets.scripts as scripts
from assets.scripts import titlebar

class Style(ttk.Style):
    def __init__(self, master):
        super().__init__(master)
        
        theme = str(master.tk.call("ttk::style", "theme", "use")).split("-")[-1]
        
        if (theme == "dark"):
            activebg = "#2f2f2f"
            pressedbg = "#232323"
            
            primarybg = "#202020"
            secondbg = "#1c1c1c"
            
            fg = "#f9f9f9" # BB86FC for purple
        
        elif (theme == "light"):
            activebg = "#EEEEEE"
            pressedbg = "#E0E0E0"
            
            primarybg = "#f9f9f9"
            secondbg = "#fff"
            
            fg = "#000"
        
        self.configure(".", font=("HP Simplified Jpan Light", 15), foreground=fg)
        self.configure("TLabel", font=("HP Simplified Jpan Light", 15), anchor="center", background=primarybg)
        self.configure("TFrame", background=primarybg)
        self.configure("TLabelframe", background=primarybg)
        
        self.configure("RootBody.TFrame", background=secondbg)
        self.configure("RootBody.TLabelframe", background=secondbg)
        
        self.configure("Titlebar.TLabel", anchor="center")
        self.configure("TitlebarButton.TLabel", anchor="center", background=primarybg)
        # self.map("TitlebarButton.TLabel", background=[("pressed", pressedbg), ("active", activebg)])
        
        
        self.configure("SidebarButton.TLabel", anchor="w", font=("HP Simplified Jpan Light", 15))
        self.map("SidebarButton.TLabel", background=[("pressed", pressedbg), ("active", activebg)])