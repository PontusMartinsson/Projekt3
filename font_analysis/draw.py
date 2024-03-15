from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

# Load the TrueType Font file
font_path = 'CourierPrime-Regular.ttf'

# Define the output directory
output_dir = 'glyph_images'
os.makedirs(output_dir, exist_ok=True)

# Set the font size and create a font object
font_size = 100
font = ImageFont.truetype(font_path, font_size)

# Create a blank canvas to render the glyphs
canvas_size = (font_size, font_size)
canvas = Image.new('L', canvas_size, color=255)
draw = ImageDraw.Draw(canvas)

# Define characters to render (you may want to include all characters in your font)
characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

# Render and analyze each glyph
i = 0
while i < characters.size:
    # Render the glyph onto the canvas
    draw.text((0, 0), char, font=font, fill=0)

    # Convert the image to binary
    glyph_array = np.array(canvas)
    binary_glyph_array = (glyph_array > 128).astype(np.uint8) * 255

    # Save the binary image
    img = Image.fromarray(binary_glyph_array)
    if(characters[i].isupper()):
        img.save(os.path.join(output_dir, (characters[i] + '_c.png')))
    else:
        img.save(os.path.join(output_dir, (characters[i] + '_l.png')))

    # Clear the canvas for the next glyph
    draw.rectangle([0, 0, font_size, font_size], fill=255)

    # Analyze pixel distribution and visualize results
    # Perform further analysis as needed
