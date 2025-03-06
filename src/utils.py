
# utils.py
# - Common helper functions: image reading, file sorting, parsing K.txt, etc.

import numpy as np

def load_images():
    images = []
    # Loop through image indices from 0 to 29 (formatted as 0000, 0001, ..., 0029)
    for i in range(30):
        filename = f"images/{i:04d}.jpg"  # Formats number with 4 digits (e.g., 0000.jpg)
        img = cv2.imread(filename)
        if img is None:
            print(f"Warning: Unable to load image {filename}")
        else:
            images.append(img)
    return images

def read_calibration_matrix():
    # Assumes K.txt contains a 3x3 matrix with one row per line.
    K = np.loadtxt("K.txt")
    return K

    