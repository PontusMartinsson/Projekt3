import os
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

def analyze(ttf_path: str, resolution: int):
    pixels = []
    font = ImageFont.truetype(ttf_path, resolution)

    # create a blank canvas to render the symbols
    canvas_size = (resolution, resolution)
    canvas = Image.new('L', canvas_size, color=255)
    draw = ImageDraw.Draw(canvas)

    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    i = 0

    while i < len(characters):
        draw.text((0, 0), characters[i], font=font, fill=0) # draw the symbol onto the canvas

        glyph_array = np.array(canvas)
        binary_glyph_array = (glyph_array > 128).astype(np.uint8) * 255
        
        img = Image.fromarray(binary_glyph_array)
        img.save('letter.png')

        img_analysis = cv2.imread('letter.png', cv2.IMREAD_GRAYSCALE)
        
        pixels.append(np.sum(img_analysis == 0))

        

        draw.rectangle([0, 0, resolution, resolution], fill=255) #clear canvas

        i += 1

    os.remove('letter.png')

    return(pixels)
