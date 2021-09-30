import tkinter as tk
from tkinter import ttk

import assets.scripts as scripts


class Sidebar(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, width=350, labelwidget=ttk.Frame())
        self.root = self.nametowidget(master.winfo_parent())
        
        self.pack_propagate(False)
        
        image = scripts.get_image
        
        size = (60, 60)
        searchImg = image("search.png", *size)
        accountImg = image("account.png", *size)
        uploadImg = image("camera.png", *size)
        messageImg = image("messages.png", *size)
        settingImg = image("options.png", *size)
        exitImg = image("shutdown.png", *size)
        
        
        # search button
        searchButton = ttk.Button(self, text="Search", image=searchImg, style="SidebarButton.TLabel", compound="left")
        searchButton.image = searchImg
        searchButton.pack(side="top", fill="x", padx=1, pady=(80,0))
        
        # account button
        accountButton = ttk.Button(self, text="Account", image=accountImg, style="SidebarButton.TLabel", compound="left")
        accountButton.image = accountImg
        accountButton.pack(side="top", fill="x", padx=1)
        
        # upload button
        uploadButton = ttk.Button(self, text="Upload", image=uploadImg, style="SidebarButton.TLabel", compound="left")
        uploadButton.image = uploadImg
        uploadButton.pack(side="top", fill="x", padx=1)
        
        # message button
        messageButton = ttk.Button(self, text="Messages", image=messageImg, style="SidebarButton.TLabel", compound="left")
        messageButton.image = messageImg
        messageButton.pack(side="top", fill="x", padx=1)
        
        # settings button
        settingsButton = ttk.Button(self, text="Options", image=settingImg, style="SidebarButton.TLabel", compound="left")
        settingsButton.image = settingImg
        settingsButton.pack(side="bottom", fill="x", padx=1)
        
        # exit button
        exitButton = ttk.Button(self, text="Exit", image=exitImg, style="SidebarButton.TLabel", compound="left")
        exitButton.image = exitImg
        exitButton.pack(side="bottom", fill="x", padx=1, pady=(0,80), before=settingsButton)
        
        
        # add spaces to all widgets
        for button in self.winfo_children():
            if (not isinstance(button, ttk.Button)):
                continue
            
            button.configure(text=" " + button["text"])