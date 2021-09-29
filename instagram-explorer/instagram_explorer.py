import tkinter as tk
from tkinter import ttk

import os
import sys
from ctypes import windll

import time
from winsound import PlaySound, SND_FILENAME
from configparser import ConfigParser

import instaloader
import instabot

import assets.scripts as scripts


class Root(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self._startTime = time.time()
        
        # setup configs
        self.configParser = ConfigParser()
        self.configParser.read("assets/config.ini")
        
        # setup instagram
        self.instaloader = instaloader.Instaloader()
        self.instabot = instabot.Bot()
        self.user = None
        
        # create body
        self.body = ttk.Frame(self, style="RootBody.TFrame")
        self.body.pack(side="bottom", fill="both", expand=True)
        
        # prepare frames
        self.shownFrame = None
        self.loadedFrames = []
        self.allFrames = {}
        for filename in os.listdir("assets/scripts/frames/"):
            if (filename == "__init__.py"):
                continue
            
            frameName = filename.replace(".py")
            self.allFrames[frameName] = eval(f"scripts.{frameName}(self.body)")
        
        
        
        
if (__name__ == "__main__"):
    application = Root()
    application.mainloop()
