import tkinter as tk
from tkinter import ttk

import instaloader
import threading

import assets.scripts as scripts

class Home(ttk.Frame):
    def __init__(self, master, root):
        super().__init__(master)
        self.root = root
        
        self.loadingPosts = False
        
        topHolder = ttk.Frame(self)
        topHolder.pack(side="top", pady=(74,0))
        
        ttk.Label(topHolder, text=self.root.title(), font=("HP Simplified Jpan Light", 20), anchor="s").pack(side="bottom", anchor="s")
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
            for index, post in enumerate(instaloader.Hashtag.from_name(self.root.instaloader.context, "memes").get_posts()):
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
                
                def set_bind(widget, _post):
                    widget.bind("<Button-1>", lambda event: self.root.loadframe("Image", post=_post))
                
                try:
                    placeholderFrame.destroy()
                    
                    postLabel = ttk.Label(self.postFrame, image=thumbnail)
                    postLabel.image = thumbnail
                    postLabel.pack(side="left", padx=10)
                    
                    set_bind(postLabel, post)
                except tk.TclError as e:
                    print(f"failed to load post {index+1} on home field - tcl error", e)
                
        except RuntimeError:
            print("cannot load home feed - run time error")
        
        except instaloader.exceptions.LoginRequiredException:
            print("cannot load home feed - login redirect")
            
        except ConnectionError:
            print("cannot load home feed - connection error")
            