import tkinter as tk
from tkinter import Variable, ttk

from instaloader.exceptions import LoginRequiredException

import assets.scripts as scripts
from assets.scripts.image_handler import get_image


class Sidebar(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, width=350, labelwidget=ttk.Frame(), style="RootBody.TLabelframe")
        self.pack_propagate(False)
        
        self.root = master
        while (str(self.root) != "."):
            self.root = self.nametowidget(self.root.winfo_parent())
            
        image = scripts.get_image        
        size = (60, 60)
        
        titleFont = ("HP Simplified Jpan Light", 20)
        entryFont = ("HP Simplified Jpan Light", 14)
        
        self._theme = tk.StringVar(value=str(self.root.tk.call("ttk::style", "theme", "use")).split("-")[-1])
        self._theme.trace_add("write", lambda *arg: self.on_theme_change())
        
        self._showPwrd = tk.BooleanVar(value=self.root.configParser.getboolean("privacy", "show_password"))
        self._showPwrd.trace_add("write", lambda *arg: self.on_password_visibility_change(size))
        
        _defaultUsername = "Username:"
        self.username = tk.StringVar(value=_defaultUsername)
        self.username.default = _defaultUsername
        
        _defaultPassword = "Password:"
        self.password = tk.StringVar(value=_defaultPassword)
        self.password.default = _defaultPassword
        
        _defaultTFA = "2FA:"
        self.tfa = tk.StringVar(value=_defaultTFA)
        self.tfa.default = _defaultTFA
        
        mainMenu = ttk.Frame(self)
        settingsMenu = ttk.Frame(self)
        accountMenu = ttk.Frame(self)
        loginMenu = ttk.Frame(self)
        
        self.menus = {"mainMenu": mainMenu, "settingsMenu": settingsMenu, "accountMenu": accountMenu,
                      "loginMenu": loginMenu}
        
        # main menu

        searchImg = image(self.root, "search.png", *size)
        accountImg = image(self.root, "account.png", *size)
        uploadImg = image(self.root, "camera.png", *size)
        messageImg = image(self.root, "messages.png", *size)
        settingImg = image(self.root, "options.png", *size)
        exitImg = image(self.root, "shutdown.png", *size)
        
        # title
        mainTitle = "Menu"
        ttk.Label(mainMenu, text=mainTitle, font=titleFont).pack(side="top", anchor="w", padx=20, pady=(79,5))
        ttk.Separator(mainMenu, orient="horizontal").pack(side="top", fill="x", padx=20, pady=(0,25))
        
        # search button
        searchButton = ttk.Button(mainMenu, text="Search", image=searchImg, style="SidebarButton.TLabel", compound="left")
        searchButton.image = searchImg
        searchButton.pack(side="top", fill="x", pady=(10,0))
        
        # account button
        accountButton = ttk.Button(mainMenu, text="Account", image=accountImg, style="SidebarButton.TLabel", compound="left", command=lambda:self.loadmenu("accountMenu"))
        accountButton.image = accountImg
        accountButton.pack(side="top", fill="x")
        
        # upload button
        uploadButton = ttk.Button(mainMenu, text="Upload", image=uploadImg, style="SidebarButton.TLabel", compound="left", state="disabled")
        uploadButton.image = uploadImg
        uploadButton.pack(side="top", fill="x")
        
        # message button
        messageButton = ttk.Button(mainMenu, text="Messages", image=messageImg, style="SidebarButton.TLabel", compound="left", state="disabled")
        messageButton.image = messageImg
        messageButton.pack(side="top", fill="x")
        
        ttk.Separator(mainMenu, orient="horizontal").pack(side="top", fill="x", padx=20, pady=25)
        
        # settings button
        settingsButton = ttk.Button(mainMenu, text="Options", image=settingImg, style="SidebarButton.TLabel", compound="left", command=lambda:self.loadmenu("settingsMenu"))
        settingsButton.image = settingImg
        settingsButton.pack(side="top", fill="x")
        
        # exit button
        exitButton = ttk.Button(mainMenu, text="Exit", image=exitImg, style="SidebarButton.TLabel", compound="left", command=self.root.close_application)
        exitButton.image = exitImg
        exitButton.pack(side="top", fill="x", pady=(0,80))
        
        
        # settings menu
        
        themeImg = get_image(self.root, "theme.png", *size)
        placeholderImg = get_image(self.root, "circle.png", *size)
        settingsBackImg = get_image(self.root, "return.png", *size)
        
        settingsTitle = "Menu > Settings"
        ttk.Label(settingsMenu, text=settingsTitle, font=titleFont).pack(side="top", anchor="w", padx=20, pady=(79,5))
        ttk.Separator(settingsMenu, orient="horizontal").pack(side="top", fill="x", padx=20, pady=(0,25))
        
        # theme buttons
        themeButton = ttk.Checkbutton(settingsMenu, image=themeImg, style="SidebarButton.TLabel", compound="left", onvalue="dark", offvalue="light", variable=self._theme)
        themeButton.image = themeImg
        themeButton.pack(side="top", fill="x", pady=(10,0))
        
        if (self._theme.get() == "light"): themeButton.configure(text="Dark Mode")
        else: themeButton.configure(text="Light Mode")
        
        # settings hide password button
        self.hidePasswordButton = ttk.Checkbutton(settingsMenu, style="SidebarButton.TLabel", compound="left", variable=self._showPwrd)
        self.hidePasswordButton.pack(side="top", fill="x")
        self.on_password_visibility_change(size)
        
        # placeholder button #1
        placeholderButton = ttk.Button(settingsMenu, text="Placeholder 1", image=placeholderImg, style="SidebarButton.TLabel", compound="left",)
        placeholderButton.image = placeholderImg
        placeholderButton.pack(side="top", fill="x")
        
        # placeholder button #2
        placeholderButton = ttk.Button(settingsMenu, text="Placeholder 2", image=placeholderImg, style="SidebarButton.TLabel", compound="left",)
        placeholderButton.image = placeholderImg
        placeholderButton.pack(side="top", fill="x")
        
        ttk.Separator(settingsMenu, orient="horizontal").pack(side="top", fill="x", padx=20, pady=25)
        
        # settings back button -> home
        settingsBackButton = ttk.Button(settingsMenu, text="Back", image=settingsBackImg, style="SidebarButton.TLabel", compound="left", command=lambda:self.loadmenu("mainMenu"))
        settingsBackButton.image = settingsBackImg
        settingsBackButton.pack(side="top", fill="x")
        
        
        # account menu
        
        viewAccImg = get_image(self.root, "account.png", *size)
        accPlaceholderImg = get_image(self.root, "circle.png", *size)
        accBackImg = get_image(self.root, "return.png", *size)
        
        accountTitle = "Menu > Account"
        ttk.Label(accountMenu, text=accountTitle, font=titleFont).pack(side="top", anchor="w", padx=20, pady=(79,5))
        ttk.Separator(accountMenu, orient="horizontal").pack(side="top", fill="x", padx=20, pady=(0,25))
        
        # view account
        viewAccountButton = ttk.Button(accountMenu, text="View Account", image=viewAccImg, style="SidebarButton.TLabel", compound="left")
        viewAccountButton.image = viewAccImg
        viewAccountButton.pack(side="top", fill="x", pady=(10,0))
        
        # log
        logButton = ttk.Button(accountMenu, style="SidebarButton.TLabel", compound="left")
        logButton.image = viewAccImg
        logButton.pack(side="top", fill="x")
        
        if (self.root.user is None):
            logImg = get_image(self.root, "login.png", *size)
            logButton.configure(text="Login", image=logImg, command=lambda:self.loadmenu("loginMenu"))
            
            viewAccountButton.configure(state="disabled")
        else:
            logImg = get_image(self.root, "logout.png", *size)
            logButton.configure(text="Logout", image=logImg, command=None)
            
            viewAccountButton.configure(state="normal")
            
        logButton.image = logImg
        
        # placeholder account
        placeholderButton = ttk.Button(accountMenu, text="placeholder 1", image=accPlaceholderImg, style="SidebarButton.TLabel", compound="left")
        placeholderButton.image = accPlaceholderImg
        placeholderButton.pack(side="top", fill="x")
        
        # placeholder account
        placeholderButton = ttk.Button(accountMenu, text="placeholder 2", image=accPlaceholderImg, style="SidebarButton.TLabel", compound="left")
        placeholderButton.image = accPlaceholderImg
        placeholderButton.pack(side="top", fill="x")
        
        ttk.Separator(accountMenu, orient="horizontal").pack(side="top", fill="x", padx=20, pady=25)
        
        # account back button -> home
        accountBackButton = ttk.Button(accountMenu, text="Back", image=accBackImg, style="SidebarButton.TLabel", compound="left", command=lambda:self.loadmenu("mainMenu"))
        accountBackButton.image = accBackImg
        accountBackButton.pack(side="top", fill="x")
        
        
        # login menu
        
        loginImg = get_image(self.root, "login.png", *size)
        loginBackImg = get_image(self.root, "return.png", *size)
        
        loginTitle = "Menu > Account"
        ttk.Label(loginMenu, text=loginTitle, font=titleFont).pack(side="top", anchor="w", padx=20, pady=(79,5))
        ttk.Separator(loginMenu, orient="horizontal").pack(side="top", fill="x", padx=20, pady=(0,25))
        
        # ttk.Entry(loginMenu, font=("HP Simplified Jpan Light", 14)).pack(side="top", fill="x", padx=10, pady=(10,5))
        # ttk.Entry(loginMenu, font=("HP Simplified Jpan Light", 14)).pack(side="top", fill="x", padx=10, pady=5)
        # ttk.Entry(loginMenu, font=("HP Simplified Jpan Light", 14)).pack(side="top", fill="x", padx=10, pady=(5, 10))

        usernameEntry = ttk.Entry(loginMenu, textvariable=self.username, font=entryFont)
        usernameEntry.pack(side="top", fill="x", padx=10, pady=(12,6))
        usernameEntry.var = self.username
        
        self.passwordEntry = ttk.Entry(loginMenu, textvariable=self.password, font=entryFont)
        self.passwordEntry.pack(side="top", fill="x", padx=10, pady=6)
        self.passwordEntry.var = self.password
        
        tfaEntry = ttk.Entry(loginMenu, textvariable=self.tfa, font=entryFont)
        tfaEntry.pack(side="top", fill="x", padx=10, pady=(6,10))
        tfaEntry.var = self.tfa
        
        usernameEntry.bind("<FocusIn>", lambda event: self.toggle_entry(usernameEntry))
        usernameEntry.bind("<FocusOut>", lambda event: self.toggle_entry(usernameEntry))
        self.passwordEntry.bind("<FocusIn>", lambda event: self.toggle_entry(self.passwordEntry))
        self.passwordEntry.bind("<FocusOut>", lambda event: self.toggle_entry(self.passwordEntry))
        tfaEntry.bind("<FocusIn>", lambda event: self.toggle_entry(tfaEntry))
        tfaEntry.bind("<FocusOut>", lambda event: self.toggle_entry(tfaEntry))
        
        # login button
        loginButton = ttk.Button(loginMenu, text="Login", image=loginImg, style="SidebarButton.TLabel", compound="left", command=None)
        loginButton.image = loginImg
        loginButton.pack(side="top", fill="x")
        
        ttk.Separator(loginMenu, orient="horizontal").pack(side="top", fill="x", padx=20, pady=25)
        
        # login back button -> account menu
        loginBackButton = ttk.Button(loginMenu, text="Back", image=loginBackImg, style="SidebarButton.TLabel", compound="left", command=lambda:self.loadmenu("accountMenu"))
        loginBackButton.image = loginBackImg
        loginBackButton.pack(side="top", fill="x")
        
        # add spaces to all widgets
        for button in self.winfo_children():
            if (not isinstance(button, (ttk.Button, ttk.Checkbutton))):
                continue
            
            button.configure(text=" " + button["text"])
            
            
        self.loadmenu("mainMenu")
            
            
    def loadmenu(self, _next) -> None:
        try: self.menu.pack_forget()
        except AttributeError: pass
        
        _next = self.menus[_next]
        _next.pack(fill="both", expand=True, padx=1, pady=2)
        self.menu = _next
        
        
    def toggle_entry(self, entry):
        var =  entry.var
        
        if (var.get() == var.default):
            var.set("")
            
            if (entry == self.passwordEntry) & (self._showPwrd.get()):
                self.passwordEntry.configure(show="*")
        
        elif (var.get() in ("", " ")):
            var.set(var.default)
            
            if (entry == self.passwordEntry):
                self.passwordEntry.configure(show="")
        
        
    def on_theme_change(self) -> None:
        self.root.on_theme_change(self._theme.get())
        
        self.root.configParser.set("appearance", "theme", self._theme.get())
        self.root.write_updated_configs()        
        
    def on_password_visibility_change(self, size) -> None:
        
        if (self._showPwrd.get()): 
            self.hidePasswordButton.configure(text="Hide Password")
            hidePassImg = get_image(self.root, "invisible.png", *size)
            try: self.passwordEntry.configure(show="")
            except AttributeError: pass
        else: 
            self.hidePasswordButton.configure(text="Show Password")
            hidePassImg = get_image(self.root, "visible.png", *size)
            try: self.passwordEntry.configure(show="*")
            except AttributeError: pass
            
        self.hidePasswordButton.configure(image=hidePassImg)
        self.hidePasswordButton.image = hidePassImg
        
        self.root.configParser.set("privacy", "show_password", str(self._showPwrd.get()))
        self.root.write_updated_configs()
