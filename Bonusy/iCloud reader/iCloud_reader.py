"""
    Reads all files in iCloud folder forcing windows to make thumbnails
"""

import os
import glob
from PIL import Image


def preload_thumbnails(directory):
    # List all jpg and png files in the directory
    full_list = glob.glob(f'{directory}/*.jpg') + glob.glob(f'{directory}/*.png')
    for index, filename in enumerate(full_list):
        try:
            # Open and immediately close the image
            print(f"Opening file {filename} ({index+1} / {len(full_list)})")
            with Image.open(filename) as img:
                pass
        except IOError:
            print(f"Cannot open {filename}")


# Replace 'path_to_your_directory' with the path to your iCloud photos directory
preload_thumbnails(r'E:\Media\Obrázky Windows\iCloud Photos\Photos')
