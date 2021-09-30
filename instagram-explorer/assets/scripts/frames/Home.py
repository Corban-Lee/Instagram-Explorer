import tkinter as tk
from tkinter import ttk

import assets.scripts as scripts

class Home(ttk.Frame):
    def __init__(self, master, root):
        super().__init__(master)
        self.root = root
        
        titleHolder = ttk.Frame(self)
        titleHolder.pack(side="top", pady=(130,0))
        
        logoImg = scripts.get_image("instagram_logo.png", 200, 200)
        logoLabel = ttk.Label(titleHolder, image=logoImg, style="TLabel")
        logoLabel.image = logoImg
        logoLabel.pack(side="left")
        
        titleLabel = ttk.Label(titleHolder, text=self.root.title(), font=("Courier New", 40), wraplength=600)
        titleLabel.pack(side="right", padx=(5,0))
        
        
        postFrame = ttk.Frame(self)
        postFrame.pack(side="bottom", pady=(0,130))
        
        ttk.LabelFrame(postFrame, width=200, height=200, labelwidget=ttk.Frame()).pack(side="left")
        ttk.LabelFrame(postFrame, width=200, height=200, labelwidget=ttk.Frame()).pack(side="left", padx=10)
        ttk.LabelFrame(postFrame, width=200, height=200, labelwidget=ttk.Frame()).pack(side="left")