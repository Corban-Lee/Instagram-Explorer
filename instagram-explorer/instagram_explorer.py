import tkinter as tk
from tkinter import ttk, font as tkfont

import os
import sys
from ctypes import windll

import time
from winsound import PlaySound, SND_FILENAME
from configparser import ConfigParser

import instaloader
import instabot

import assets.scripts as scripts


# Windows OS styles for custom taskbar integration
GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080


windll.shcore.SetProcessDpiAwareness(1)


class Root(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self._startTime = time.time()
        
        # setup configs
        self.configParser = ConfigParser()
        self.configParser.read("assets/config.ini")
        
        # prepare window
        self.overrideredirect(True)
        self.after(10, self.set_app_window)
        self.bind("<Map>", self.frame_mapped)
        self.z = 0
        
        # setup style
        self.tk.call("source", "assets/theme/sun-valley.tcl")
        self.tk.call("set_theme", "light")
        self.style = scripts.Style(self)
        self.configure(borderwidth=1, relief="solid")
        
        # setup window
        self.title("Instagram Explorer")
        self.iconbitmap("assets/images/logo.ico")
        self.geometry("1280x800")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.close_application)
        
        # position window to center of screen
        user32 = windll.user32
        screenW, screenH = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        x = int(screenW / 2) - int(self.winfo_width() / 2)
        y = int(screenH / 2) - int(self.winfo_height() / 2)
        self.geometry(f'+{x}+{y}')
        
        # setup instagram
        self.instaloader = instaloader.Instaloader()
        self.instabot = instabot.Bot()
        self.user = None
        
        # setup titlebar
        self.titlebar = scripts.Titlebar(self)
        self.titlebar.pack(side="top", fill="x", padx=10, pady=10)
        
        # create body
        self.body = ttk.Frame(self, style="RootBody.TFrame")
        self.body.pack(side="bottom", fill="both", expand=True)
        
        # create sidebar
        self.sidebar = scripts.Sidebar(self.body)
        self.sidebar.pack(side="left", fill="y", padx=(10,0), pady=(0,10))
        
        # create scrollbar
        scrollFrame = ttk.LabelFrame(self.body, labelwidget=ttk.Frame())
        scrollFrame.pack(side="right", fill="y", pady=(0,10), padx=(0,10))
        
        self.scrollbar = ttk.Scrollbar(scrollFrame, orient="vertical", style="NoTrough.TScrollbar")
        self.scrollbar.pack(fill="y", padx=1, pady=2, expand=True)
        
        # create frame holder
        self.frameHolder = ttk.LabelFrame(self.body, labelwidget=ttk.Frame())
        self.frameHolder.pack(side="right", fill="both", expand=True, padx=10, pady=(0,10))
        
        # prepare frames
        self.shownFrame = None
        self.allFrames = {}
        for filename in os.listdir("assets/scripts/frames/"):
            if (filename.startswith("_")):
                continue
            
            frameName = filename.replace(".py", "")
            self.allFrames[frameName] = eval(f"scripts.{frameName}(master=self.frameHolder, root=self)")
            
        self.loadframe("Home")
            
            
    def loadframe(self, frameName:str, **kw):
        try:
            self.shownFrame.pack_forget()
            self.shownFrame.unload()
        except AttributeError:
            pass
        
        self.shownFrame = self.allFrames[frameName]
        self.shownFrame.pack(fill="both", expand=True, padx=2, pady=2)
        
        try:
            self.shownFrame.load(**kw)
        except AttributeError:
            pass
            
            
    def close_application(self) -> None:
        sys.exit()    
        
    def set_app_window(self) -> None:
        hwnd = windll.user32.GetParent(self.winfo_id())
        stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        stylew = stylew & ~WS_EX_TOOLWINDOW
        stylew = stylew | WS_EX_APPWINDOW
        windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)
                               
        self.wm_withdraw()
        self.after(10, self.wm_deiconify)
        
        
    def frame_mapped(self, event) -> None:
        self.overrideredirect(True)
        
        if (self.z == 0):
            self.set_app_window()
            self.z = 1
        
        
        
if (__name__ == "__main__"):
    application = Root()
    application.mainloop()
