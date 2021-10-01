import tkinter as tk
from tkinter import ttk

import instaloader
import threading

import assets.scripts as scripts
from assets.scripts.titlebar import Titlebar

class Home(ttk.Frame):
    def __init__(self, master, root):
        super().__init__(master)
        self.root = root
        
        self.loadingPosts = False
        
        topHolder = ttk.Frame(self)
        topHolder.pack(side="top", pady=(74,0))
        
        ttk.Label(topHolder, text=self.root.title(), font=("HP Simplified Jpan Light", 20), anchor="s").pack(side="bottom", anchor="s")
        
        # logoImg = scripts.get_image("instagram_logo.png", 200, 200)
        # logoLabel = ttk.Label(topHolder, image=logoImg, style="TLabel")
        # logoLabel.image = logoImg
        # logoLabel.pack(side="right")
        
        # _title = str(self.root.title()).split(" ")
        
        # titleHolder = ttk.Frame(topHolder)
        # titleHolder.pack(side="left", padx=(0,35))
        
        # ttk.Label(titleHolder, text=_title[0], font=("HP Simplified Jpan Light", 40), anchor="e").pack(side="top", anchor="e")
        # ttk.Label(titleHolder, text=_title[1], font=("HP Simplified Jpan Light", 40), anchor="e").pack(side="bottom", anchor="e")
        
        # titleLabel = ttk.Label(titleHolder, text=_title, font=("HP Simplified Jpan Light", 40), wraplength=600)
        # titleLabel.pack(side="right", padx=(40,0))
        
        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=60, pady=(10,0))
        
        self.postFrame = ttk.Frame(self)
        self.postFrame.pack(side="bottom", pady=(0,80))
        threading.Thread(target=self.load_posts).start()
        
        
    def unload(self) -> None:
        self.loadingPosts = False
        
        
    def load_posts(self) -> None:
        width, height = 255, 255
        limit = 3
        
        self.loadingPosts = True
        
        try:
            for index, post in enumerate(instaloader.Hashtag.from_name(self.root.instaloader.context, "instagram").get_posts()):
                if (index == limit):
                    break
                
                if (not self.loadingPosts):
                    break
                
                placeholderFrame = ttk.LabelFrame(self.postFrame, width=width, height=height, labelwidget=ttk.Frame())
                placeholderFrame.pack(side="left", padx=10)
                placeholderFrame.pack_propagate(False)
                
                progressbar = scripts.ProgressCircle(placeholderFrame, (width/3, height/3))
                progressbar.pack(fill="both", expand=True, padx=5, pady=5)
                progressbar.start()
                
                thumbnail = scripts.get_image(self.root, post.url, width=width, height=height, mode="url", roundCornerRadius=12, cropToSize=True)
                
                if (not self.loadingPosts):
                    break
                
                try:
                    placeholderFrame.destroy()
                    
                    postLabel = ttk.Label(self.postFrame, image=thumbnail)
                    postLabel.image = thumbnail
                    postLabel.pack(side="left", padx=10)
                except tk.TclError:
                    pass
        except RuntimeError:
            pass
        
        except instaloader.exceptions.LoginRequiredException:
            print("cannot load home feed - login redirect")
            