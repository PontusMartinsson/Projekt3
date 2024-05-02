import os
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from alive_progress import alive_bar

def analyze(characters, resolution):
    pixels = []
    font = ImageFont.truetype("font.ttf", resolution)

    # characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789#*+-=.,!?%&~/$@ " #default characters
    char_list = list(characters)

    # create a blank canvas to render the symbols
    canvas_size = (resolution, resolution)
    canvas = Image.new("L", canvas_size, color=255)
    draw = ImageDraw.Draw(canvas)

    with alive_bar(len(characters)) as bar:
        for char in char_list:
            draw.text((0, 0), char, font=font, fill=0) # draw the symbol onto the canvas

            glyph_array = np.array(canvas)
            binary_glyph_array = (glyph_array > 128).astype(np.uint8) * 255
            
            img = Image.fromarray(binary_glyph_array)
            img.save("letter.png")

            img_analysis = cv2.imread("letter.png", cv2.IMREAD_GRAYSCALE)
            
            pixels.append(np.sum(img_analysis == 0))

            draw.rectangle([0, 0, resolution, resolution], fill=255) #clear canvas

            bar()

    i = 0

    while i < len(pixels):
        j = 1

        while j < len(pixels) - i:
            if pixels[j] > pixels[j-1]:
                pixels[j], pixels[j-1] = pixels[j-1], pixels[j]
                char_list[j], char_list[j-1] = char_list[j-1], char_list[j]

            j += 1
        
        i += 1

    os.remove("letter.png")

    characters = "".join(char_list)

    return characters
