import tkinter as tk
from tkinter import ttk

import instaloader
import threading

import assets.scripts as scripts


class Image(ttk.Frame):
    def __init__(self, master, root):
        super().__init__(master)
        self.root = root
        
        # self.loadingFrame = ttk.LabelFrame(self, labelwidget=ttk.Frame(), width=500, height=500)
        # self.loadingCircle = scripts.ProgressCircle(self.loadingFrame, (100, 100))
        # self.loadingCircle.place(relx=0.5, rely=0.5, anchor="center")
        
        # self.imageLabel = ttk.Label(self)
        
        self.likes = tk.IntVar()
        self.comments = tk.IntVar()
        
        header = ttk.Frame(self)
        header.pack(side="top", fill="both", expand=True)
        
        ttk.Separator(self, orient="horizontal").pack(side="top", fill="x", padx=30)
        
        body = ttk.Frame(self)
        body.pack(side="bottom", fill="both")
    
        stats = ttk.Frame(body)
        stats.pack(side="right", fill="both", expand=True, pady=10)
        
        likeButton = ttk.Button(stats, text="Like", style="Image.TButton")
        likeButton.pack(side="top", fill="x", padx=10)
        
        commentButton = ttk.Button(stats, text="Comment", style="Image.TButton")
        commentButton.pack(side="top", fill="x", padx=10, pady=10)
        
        self.likes.trace_add("write", lambda *arg: likeButton.configure(text=f"Like - {self.likes.get()}"))
        self.comments.trace_add("write", lambda *arg: commentButton.configure(text=f"Comment - {self.comments.get()}"))
        
        ttk.Button(stats, text="Back", style="Image.TButton", command=lambda:self.root.loadframe("Home")).pack(side="top", fill="x", padx=10)
        
        self.imageLabel = ttk.Label(body)
        

        
    def load(self, post):
        self.imageLabel.place_forget()
        # self.loadingFrame.place(relx=0.5, rely=0.5, anchor="center")
        # self.loadingCircle.start()
        
        self.likes.set(post.likes)
        self.comments.set(post.comments)
        
        print(post.likes)

        def thread():
            image = scripts.get_image(self.root, post.url, 500, 500, mode="url", roundCornerRadius=25, cropToSize=True)
            
            # self.loadingFrame.pack_forget()
            # self.loadingCircle.stop()
            
            self.imageLabel.configure(image=image)
            self.imageLabel.image = image
            self.imageLabel.pack(side="left", fill="both", padx=10, pady=10)
            
        threading.Thread(target=thread).start()
