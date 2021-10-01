import tkinter as tk
from tkinter import ttk

import assets.scripts as scripts
from assets.scripts.image_handler import get_image


class Sidebar(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, width=350, labelwidget=ttk.Frame())
        
        self.root = master
        while (str(self.root) != "."):
            self.root = self.nametowidget(self.root.winfo_parent())
        
        self.pack_propagate(False)
        
        image = scripts.get_image
        size = (60, 60)
        
        mainMenu = ttk.Frame(self)
        settingsMenu = ttk.Frame(self)
        
        # main menu

        searchImg = image(self.root, "search.png", *size)
        accountImg = image(self.root, "account.png", *size)
        uploadImg = image(self.root, "camera.png", *size)
        messageImg = image(self.root, "messages.png", *size)
        settingImg = image(self.root, "options.png", *size)
        exitImg = image(self.root, "shutdown.png", *size)
        
        # title
        mainTitle = "Menu"
        ttk.Label(mainMenu, text=mainTitle, font=("HP Simplified Jpan Light", 20)).pack(side="top", anchor="w", padx=20, pady=(79,5))
        ttk.Separator(mainMenu, orient="horizontal").pack(side="top", fill="x", padx=20, pady=(0,25))
        
        # search button
        searchButton = ttk.Button(mainMenu, text="Search", image=searchImg, style="SidebarButton.TLabel", compound="left")
        searchButton.image = searchImg
        searchButton.pack(side="top", fill="x", pady=(10,0))
        
        # account button
        accountButton = ttk.Button(mainMenu, text="Account", image=accountImg, style="SidebarButton.TLabel", compound="left")
        accountButton.image = accountImg
        accountButton.pack(side="top", fill="x")
        
        # upload button
        uploadButton = ttk.Button(mainMenu, text="Upload", image=uploadImg, style="SidebarButton.TLabel", compound="left")
        uploadButton.image = uploadImg
        uploadButton.pack(side="top", fill="x")
        
        # message button
        messageButton = ttk.Button(mainMenu, text="Messages", image=messageImg, style="SidebarButton.TLabel", compound="left")
        messageButton.image = messageImg
        messageButton.pack(side="top", fill="x")
        
        ttk.Separator(mainMenu, orient="horizontal").pack(side="top", fill="x", padx=20, pady=25)
        
        # settings button
        settingsButton = ttk.Button(mainMenu, text="Options", image=settingImg, style="SidebarButton.TLabel", compound="left", command=lambda:self.loadmenu(settingsMenu))
        settingsButton.image = settingImg
        settingsButton.pack(side="top", fill="x")
        
        # exit button
        exitButton = ttk.Button(mainMenu, text="Exit", image=exitImg, style="SidebarButton.TLabel", compound="left")
        exitButton.image = exitImg
        exitButton.pack(side="top", fill="x", pady=(0,80))
        
        
        # settings menu
        
        themeImg = get_image(self.root, "theme.png", *size)
        settingsBackImg = get_image(self.root, "return.png", *size)
        
        settingsTitle = "Menu > Settings"
        ttk.Label(settingsMenu, text=settingsTitle, font=("HP Simplified Jpan Light", 20)).pack(side="top", anchor="w", padx=20, pady=(79,5))
        ttk.Separator(settingsMenu, orient="horizontal").pack(side="top", fill="x", padx=20, pady=(0,25))
        
        self._theme = tk.StringVar(value=str(self.root.tk.call("ttk::style", "theme", "use")).split("-")[-1])
        
        # theme buttons
        themeButton = ttk.Checkbutton(settingsMenu, image=themeImg, style="SidebarButton.TLabel", compound="left", onvalue="dark", offvalue="light", variable=self._theme)
        themeButton.image = themeImg
        themeButton.pack(side="top", fill="x")
        
        if (self._theme.get() == "light"):
            themeButton.configure(text="Dark Mode")
        else:
            themeButton.configure(text="Light Mode")
        
        self._theme.trace_add("write", lambda *arg: self.on_theme_change(themeButton, size))
        
        # settings back button -> home
        settingsBackButton = ttk.Button(settingsMenu, text="Back", image=settingsBackImg, style="SidebarButton.TLabel", compound="left", command=lambda:self.loadmenu(mainMenu))
        settingsBackButton.image = settingsBackImg
        settingsBackButton.pack(side="bottom", fill="x", pady=(0,80))
        
        
        # add spaces to all widgets
        for button in self.winfo_children():
            if (not isinstance(button, ttk.Button)):
                continue
            
            button.configure(text=" " + button["text"])
            
            
        self.loadmenu(mainMenu)
            
            
    def loadmenu(self, _next) -> None:
        try: self.menu.pack_forget()
        except AttributeError: pass
        _next.pack(fill="both", expand=True, padx=1, pady=2)
        self.menu = _next
        
        
    def on_theme_change(self, button, size:tuple) -> None:
        self.root.on_theme_change(self._theme.get())
