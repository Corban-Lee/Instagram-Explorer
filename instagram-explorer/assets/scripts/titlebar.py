import tkinter as tk
from tkinter import ttk

import assets.scripts as scripts


class Titlebar(ttk.LabelFrame):
    def __init__(self, master, root) -> None:
        super().__init__(master, labelwidget=ttk.Frame(), style="RootBody.TLabelframe")
        self.root = root

        self.pack_propagate(False)
        self.configure(height=60)
        self.bind("<Button-1>", self.drag_window)
        
        self.body = ttk.Frame(self)
        self.body.pack(fill="both", expand=True, padx=3, pady=1)
        self.body.bind("<Button-1>", self.drag_window)
        
        size = (45, 45)
        
        closeImg = scripts.get_image(root, "close.png", *size)
        closeActiveImg = scripts.get_image(root, "close_active.png", *size)
        closePressedImg = scripts.get_image(root, "close_pressed.png", *size)

        minImg = scripts.get_image(root, "minimize.png", *size)
        minActiveImg = scripts.get_image(root, "minimize_active.png", *size)
        minPressedImg = scripts.get_image(root, "minimize_pressed.png", *size)
        
        closeButton = ttk.Button(self.body, style="TitlebarButton.TLabel", takefocus=False, command=root.close_application)
        closeButton.pack(side="right", padx=8)
        
        self.dynamic_image_style(closeButton, normal=closeImg, active=closeActiveImg, pressed=closePressedImg)
        
        minimizeButton = ttk.Button(self.body, style="TitlebarButton.TLabel", takefocus=False, command=self.minimize_window)
        minimizeButton.pack(side="right", padx=8)
        
        self.dynamic_image_style(minimizeButton, normal=minImg, active=minActiveImg, pressed=minPressedImg)
        
        # titleLabel = ttk.Label(self.body, text=self.root.title(), style="Titlebar.TLabel", font=("HP Simplified Jpan Light", 15))
        # titleLabel.pack(side="left", padx=15)
        # titleLabel.bind("<Button-1>", self.drag_window)
        
        
    def dynamic_image_style(self, button, normal, active, pressed) -> None:
        
        def update(image):
            button.configure(image=image)
            button.image = image
        
        button.bind("<Leave>", lambda event: update(normal))
        button.bind("<Enter>", lambda event: update(active))
        button.bind("<Button-1>", lambda event: update(pressed))
        
        update(normal)
        
        
    def drag_window(self, event) -> None:
        startX, startY = event.x_root, event.y_root
        winX, winY = self.root.winfo_x() - startX, self.root.winfo_y() - startY
        
        def move_window(event) -> None:
            x, y = event.x_root + winX, event.y_root + winY
            self.root.geometry(f'+{x}+{y}')
            
        event.widget.bind('<B1-Motion>', move_window)
        
      
    def minimize_window(self) -> None:  
        self.root.state('withdrawn')
        self.root.overrideredirect(False)
        self.root.state('iconic')
        self.root.z = 0



if __name__ == "__main__":
    root = tk.Tk()
    root.titlebar = Titlebar(root)
    root.titlebar.pack(side="top", fill="x")
    root.mainloop()

        
        
