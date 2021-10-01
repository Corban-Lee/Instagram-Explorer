from typing import Literal
from urllib.request import urlopen
from urllib.error import URLError
from PIL import Image, ImageTk, ImageDraw, ImageFilter
from io import BytesIO

IMAGE_PATH = 'assets/images'


def get_image(root, source:str,
              width:int, height:int,
              mode:Literal['path', 'url']='path',
              maketk:bool=True, roundCornerRadius:int=0, makeCircle:bool=False,
              rotation:int=0, cropToSize:bool=False,
              urlRetries:int=3
              ):
    
    """Gets an image from specified path or url (auto fills path to image directory)
    
    Options:
    \nsource            - path or url to image
    \nmode              - path or url
    \nwidth and height
    \nmaketk            - make image object tkinter compatible
    \nroundCornerRadius - radius of rounded edges (0 is off, 12 is good for smooth corners)
    \nmakeCircle        - crop image into a transparent circle
    \nrotation          - return the image rotated by this value
    \ncropToSize        - crops image to width/height arguments (sometimes produces black bars)"""


    theme = str(root.tk.call("ttk::style", "theme", "use")).split("-")[-1]
    width, height = int(width), int(height)  # pillow only excepts integers for resizing
    
    if (mode == 'path'):
        path = f"{IMAGE_PATH}/{theme}/{source}"
        image = Image.open(fp=path)
        
    elif (mode == 'url'):
        try: 
            with urlopen(source) as u: rawData = u.read()
            image = Image.open(BytesIO(rawData))
        except URLError as e:
            image = get_image(source=source, width=width, height=height, mode='url', urlRetries=urlRetries-1, maketk=False)
    
    else:
        raise TypeError(f"mode {mode} is invalid")
    
    if (cropToSize):
        image = crop(image, width, height)
    
    image = image.resize((width, height), Image.ANTIALIAS)
    
    if (roundCornerRadius > 0) & (not makeCircle):
        image = cut_corners(image, roundCornerRadius)
        
    if (makeCircle) & (roundCornerRadius <= 0):
        image = mask_circle_transparent(image, 4)
        
    if (rotation != 0):
        image = rotate_image(image, rotation)
    
    try:
        if (maketk): return ImageTk.PhotoImage(image)
        else:        return image
    except RuntimeError:
        return image
    
    
def crop(image, width, height):
    cropW, cropH = width * 20, height * 20
    imageW, imageH = image.size        
    
    while (cropW > imageW):
        cropW -= 10
        
    while (cropH > imageH):
        cropH -= 10
        
    if (width == height) & (cropW > cropH):
        cropW = cropH
        
    elif (width == height) & (cropW < cropH):
        cropH = cropW
        
    left = int((imageW-cropW) // 2)
    top = int((imageH-cropH) // 2)
    right = int((imageW+cropW) // 2)
    bottom = int((imageH+cropH) // 2)
    image = image.crop((left, top, right, bottom))
    return image
    
    
def cut_corners(image, rad):
    """Trims corners of square image to round edges"""
    
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', image.size, "white")
    w, h = image.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    image.putalpha(alpha)
    
    # TODO: apply filter to rounded corners so they arent rough
    
    return image


def mask_circle_transparent(pil_img, blur_radius, offset=0):
    """Crops image into circle with transparent background"""
    
    offset = blur_radius * 2 + offset
    mask = Image.new('L', pil_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(2))
    
    result = pil_img.copy()
    result.putalpha(mask)
    return result


def rotate_image(image, rotation):
    return image.rotate(rotation)