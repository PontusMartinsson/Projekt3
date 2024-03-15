import os
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

def test():
    font_size = 1000
    font = ImageFont.truetype('CourierPrime-Regular.ttf', font_size)

    # create a blank canvas to render the symbols
    canvas_size = (font_size, font_size)
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
        n_black = np.sum(img_analysis == 0)

        print(characters[i])
        print('Number of black pixels:', n_black)
        print("-------------------------------------")

        draw.rectangle([0, 0, font_size, font_size], fill=255) #clear canvas

        i += 1

    os.remove('letter.png')
