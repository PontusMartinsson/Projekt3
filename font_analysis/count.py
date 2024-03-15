import os
import cv2
import numpy as np

str_directory = "glyph_images"
directory = os.fsencode(str_directory)

def count(directory, filename):
    img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    n_black = np.sum(img == 0)
    print(file)
    print('Number of black pixels:', n_black)
    print("-------------------------------------")


    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    count(os.path.join(str_directory, filename))