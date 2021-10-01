from tkinter import ttk


class Style(ttk.Style):
    def __init__(self, master):
        super().__init__(master)
        
        theme = str(master.tk.call("ttk::style", "theme", "use")).split("-")[-1]
        
        if (theme == "dark"):
            activebg = "#2f2f2f"
            pressedbg = "#232323"
            secondbg = "#202020"
        
        elif (theme == "light"):
            activebg = "#EEEEEE"
            pressedbg = "#E0E0E0"
            secondbg = "#FAF9F6"
        
        self.configure(".", font=("HP Simplified Jpan Light", 15))
        self.configure("TLabel", font=("HP Simplified Jpan Light", 15), anchor="center")
        
        self.configure("RootBody.TFrame", background=secondbg)
        
        self.configure("Titlebar.TLabel", anchor="center")
        self.configure("TitlebarButton.TLabel", anchor="center")
        self.map("TitlebarButton.TLabel", background=[("pressed", pressedbg), ("active", activebg)])
        
        
        self.configure("SidebarButton.TLabel", anchor="w", font=("HP Simplified Jpan Light", 15))
        self.map("SidebarButton.TLabel", background=[("pressed", pressedbg), ("active", activebg)])