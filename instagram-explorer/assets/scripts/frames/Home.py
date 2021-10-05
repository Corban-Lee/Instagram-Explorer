import tkinter as tk
from tkinter import ttk

import instaloader
import threading
import random
import datetime

import assets.scripts as scripts

THUMBNAIL_W, THUMBNAIL_H = 160, 160
POSTFRAME_W, POSTFRAME_H = 350, None


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
        
        tags = ["Programming", "Computer", "Gaming", "Crypto", "News"]
        chosenPTag = random.choice(tags)
        tags.remove(chosenPTag)
        chosenNTag = random.choice(tags)
        
        postFrame = ttk.Frame(self)
        postFrame.pack(side="bottom", fill="y", expand=True)
        
        popularFrame = ttk.LabelFrame(postFrame, labelwidget=ttk.Button(text=f" Popular on #{chosenPTag} ", style="TLabel"), width=350)
        popularFrame.pack(side="left", fill="y", padx=(0,30), pady=60)
        
        popularHashtag = lambda: instaloader.Hashtag.from_name(self.root.instaloader.context, chosenPTag).get_top_posts()
        
        try: threading.Thread(target=lambda:self.populate_frame(frame=popularFrame, _with=popularHashtag, _amt=4)).start()
        except tk.TclError: pass
        except RuntimeError: pass

        newFrame = ttk.LabelFrame(postFrame, labelwidget=ttk.Button(text=f" New on #{chosenNTag} ", style="TLabel"), width=350)
        newFrame.pack(side="left", fill="y", pady=60)
        
        newHashtag = lambda: instaloader.Hashtag.from_name(self.root.instaloader.context, chosenNTag).get_posts()
        
        try: threading.Thread(target=lambda:self.populate_frame(frame=newFrame, _with=newHashtag, _amt=4)).start()
        except tk.TclError: pass
        except RuntimeError: pass
    
        
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
            
        # message += " User,"
        self.welcomeMessage.set(message)
        return message
    
    
    def on_new_content(self, widget:ttk.Label) -> None:
        parent = self.nametowidget(widget.winfo_parent())
        parent.grid_propagate(True)
        
        def check():
            if (parent.winfo_width() < POSTFRAME_W):
                parent.grid_propagate(False)
                parent.configure(width=POSTFRAME_W)
                
        self.root.after(5, check)
                
        
        
    def populate_frame(self, frame, _with, _amt) -> None:
        col = 0
        row = 0
        try: iterable = _with()
        except instaloader.exceptions.LoginRequiredException: pass # return print("login required")
        for index, post in enumerate((1,2,3,4,5,6,7,8)): # enumerate(iterable):
            if (index >= _amt):
                break
            
            match col: 
                case 0: padx = 10
                case _: padx = (0, 10)

            match row:
                case 0: pady=(10,0)
                case 1: pady=10
                # case _: pady=(0,10)
            
            postFrame = ttk.LabelFrame(frame, labelwidget=ttk.Frame(), width=THUMBNAIL_W, height=THUMBNAIL_H)
            postFrame.grid(column=col, row=row, padx=padx, pady=pady)
            
            if (index == 0):
                self.on_new_content(postFrame)
            
            # postLabel = self.get_post(master=frame, post=post, width=THUMBNAIL_W, height=THUMBNAIL_H)
            # postLabel.grid(column=col, row=row, padx=padx, pady=pady)
            
            col += 1
            if (col == 2):
                col, row = 0, row+1
                
                
    def get_post(self, master, post, width, height) -> ttk.Label:
        print("getting image")
        thumbnailImage = scripts.get_image(self.root, source=post.url, width=width, height=height, mode="url", roundCornerRadius=20, cropToSize=True)
        label = ttk.Label(master, image=thumbnailImage)
        label.image = thumbnailImage
        
        return label
    
        
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
            