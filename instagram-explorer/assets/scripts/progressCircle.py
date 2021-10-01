import tkinter as tk
from tkinter import ttk
from typing import Literal

import assets.scripts as scripts

        
class CustomProgressBar(ttk.Frame):
    def __init__(self, master, filename:str, size:tuple, rotations:tuple, direction:Literal['left', 'right']):
        super().__init__(master)
        self._active = False
        
        root = master
        while (str(root) != "."):
            root = self.nametowidget(root.winfo_parent())

        self.progressImageLabel = ttk.Label(self)
        self._images = [scripts.get_image(root,
                                          source=filename, 
                                          width=size[0], height=size[1],
                                          rotation=rotation) for rotation in rotations]
        
        if (direction == 'right'): self._images = list(reversed(self._images))
        
        # update progress circle image to first image and display it
        self.progressImageLabel.configure(image=self._images[0])
        self.progressImageLabel.image = self._images[0]
        self.progressImageLabel.pack(fill='both', expand=True)
        
        
    def start(self, interval:int=100) -> None:
        self._active = True
        
        def next_image(currentImageNumber:int):
            currentImageNumber += 1
            if (currentImageNumber > len(self._images) - 1):
                currentImageNumber = 0
                
            image = self._images[currentImageNumber]
            try:
                self.progressImageLabel.configure(image=image)
                self.progressImageLabel.image = image
            except tk.TclError:
                # rare: raised when loading has finished and load window is unloaded
                pass
            
            if (self._active): 
                self.after(interval, lambda:next_image(currentImageNumber))
                
        next_image(0)
        
        
    def stop(self) -> None:
        self._active = False
        
        
        
class ProgressCircle(CustomProgressBar):
    def __init__(self, master, size:tuple=(50,50)):
        super().__init__(master, filename='loader.png', size=size, 
                         rotations=(0, 45, 90, 135, 180, 225, 270, 315), direction='right')
        
        
class ProgressLogo(CustomProgressBar):
    def __init__(self, master, size:tuple=(50,50)):
        _range = (0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100,
                  105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200,
                  205, 210, 215, 220, 225, 230, 235, 240, 245, 250, 255, 260, 265, 270, 275, 280, 285, 290, 295, 300,
                  305, 310, 315, 320, 325, 330, 335, 340, 345, 350, 355, 360, 360, 360, 360, 360, 360, 360, 360, 360,
                  360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360, 360)
        super().__init__(master, filename='instagram_logo.png', size=size,
                         rotations=_range, direction='right')
        
        