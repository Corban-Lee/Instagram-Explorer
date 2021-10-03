import tkinter as tk
from tkinter import ttk

import instaloader
import threading
import random
import datetime

import assets.scripts as scripts

class Home(ttk.Frame):
    def __init__(self, master, root):
        super().__init__(master)
        self.root = root
        
        self.loadingPosts = False
        
        topHolder = ttk.Frame(self)
        topHolder.pack(side="top", fill="x", padx=30, pady=(81,0))
        
        self.welcomeMessage = tk.StringVar()
        self.clock = tk.StringVar()
        self.updatingClock = False
        
        ttk.Label(topHolder, textvariable=self.welcomeMessage, font=("HP Simplified Jpan Light", 20), anchor="s").pack(side="left", anchor="s")
        ttk.Label(topHolder, textvariable=self.clock, font=("HP Simplified Jpan Light", 20), anchor="s").pack(side="right", anchor="s")
        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=20, pady=(5,0))
        
        self.postFrame = ttk.Frame(self)
        self.postFrame.pack(side="bottom", pady=(0,80))
        # threading.Thread(target=self.load_posts).start()
        
        
    def load(self) -> None:
        self.updatingClock = True
        self.update_clock()
        
        self.update_welcome_message()
        
        
    def unload(self) -> None:
        self.loadingPosts = False
        
        
    def update_clock(self) -> None:
        if (not self.updatingClock): return
        _time = datetime.datetime.now().strftime("%A, %H:%M:%S")
        self.clock.set(_time)
        self.root.after(1000, self.update_clock)
        
        
    def update_welcome_message(self) -> str:
        hour = datetime.datetime.now().hour
        
        if (hour < 12):                     message = "Good Morning"
        elif (hour >= 12) & (hour < 18):    message = "Good Afternoon"
        elif (hour >= 18) & (hour < 22):    message = "Good Evening"
        else:                               message = "Good Night"
            
        message += " User,"
        self.welcomeMessage.set(message)
        return message
        
        
        
    def load_posts(self) -> None:
        width, height = 190, 190
        limit = 6
        
        self.loadingPosts = True
        
        hashtags = ("Memes", "Programming")
        hashtag = random.choice(hashtags)
        print(hashtag)
        
        top = ttk.Frame(self.postFrame)
        top.pack(side="top", pady=(0,10))
        
        bottom = ttk.Frame(self.postFrame)
        bottom.pack(side="bottom", pady=(10,0))
        
        try:
            for index, post in enumerate(instaloader.Profile.from_username(self.root.instaloader.context, "instagram").get_posts()):
                if (index == limit):
                    break
                
                if (not self.loadingPosts):
                    break

                if (len(top.winfo_children()) == 3):
                    parent = bottom
                
                else:
                    parent = top
                                
                placeholderFrame = ttk.LabelFrame(parent, width=width, height=height, labelwidget=ttk.Frame())
                placeholderFrame.pack(side="left", padx=10)
                placeholderFrame.pack_propagate(False)
                
                progressbar = scripts.ProgressCircle(placeholderFrame, (width/3, height/3))
                progressbar.pack(fill="both", expand=True, padx=5, pady=5)
                progressbar.start()
                
                thumbnail = scripts.get_image(self.root, post.url, width=width, height=height, mode="url", roundCornerRadius=100, cropToSize=True)
                
                if (not self.loadingPosts):
                    break
                
                def set_bind(widget, _post):
                    widget.bind("<Button-1>", lambda event: self.root.loadframe("Image", post=_post))
                
                try:
                    placeholderFrame.destroy()
                    
                    postLabel = ttk.Label(parent, image=thumbnail)
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
            