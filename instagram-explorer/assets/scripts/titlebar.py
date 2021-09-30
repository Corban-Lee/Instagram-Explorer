import tkinter as tk
from tkinter import ttk

import assets.scripts as scripts


class Titlebar(ttk.LabelFrame):
    def __init__(self, master) -> None:
        super().__init__(master, labelwidget=ttk.Frame())
        
        self.pack_propagate(False)
        self.configure(height=60)
        self.bind("<Button-1>", self.drag_window)
        
        self.body = ttk.Frame(self)
        self.body.pack(side="top", fill="both", expand=True, padx=(3,3), pady=1)
        self.body.bind("<Button-1>", self.drag_window)
        
        closeImg = scripts.get_image("close.png", 30, 30)
        maxImg = scripts.get_image("maximize.png", 30, 30)
        resImg = scripts.get_image("restore.png", 30, 30)
        minImg = scripts.get_image("minimize.png", 30, 30)
        iconImg = scripts.get_image("logo.png", 40, 40)
        
        closeButton = ttk.Button(self.body, image=closeImg, style="TitlebarButton.TLabel", takefocus=False, command=self.master.close_application)
        closeButton.image = closeImg
        closeButton.pack(side="right", fill="y", ipadx=16)
        
        # maximizeButton = ttk.Button(self.body, image=maxImg, style="TitlebarButton.TLabel", takefocus=False, command=None)
        # maximizeButton.image = maxImg
        # maximizeButton.pack(side="right", fill="y", ipadx=16)
        
        minimizeButton = ttk.Button(self.body, image=minImg, style="TitlebarButton.TLabel", takefocus=False, command=self.minimize_window)
        minimizeButton.image = minImg
        minimizeButton.pack(side="right", fill="y", ipadx=16)
        
        titleLabel = ttk.Label(self.body, text=self.master.title(), style="Titlebar.TLabel", font=("HP Simplified Hans Light", 12))
        titleLabel.pack(side="left", fill="y", padx=10)
        titleLabel.bind("<Button-1>", self.drag_window)
        
        # logoLabel = ttk.Label(self.body, image=iconImg, style="Titlebar.TLabel")
        # logoLabel.image = iconImg
        # logoLabel.pack(side="left", padx=(15,5), before=titleLabel)
        
        
    def drag_window(self, event) -> None:
        startX, startY = event.x_root, event.y_root
        winX, winY = self.master.winfo_x() - startX, self.master.winfo_y() - startY
        
        def move_window(event) -> None:
            x, y = event.x_root + winX, event.y_root + winY
            self.master.geometry(f'+{x}+{y}')
            
        event.widget.bind('<B1-Motion>', move_window)
        
      
    def minimize_window(self) -> None:  
        self.master.state('withdrawn')
        self.master.overrideredirect(False)
        self.master.state('iconic')
        self.master.z = 0


        
        
