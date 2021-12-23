import os 
import sys
import glob
import re
from typing import List
from PIL import Image
from tqdm import tqdm

def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def createGif(dirPath: str, pathGif):
    path_list = sorted(
        glob.glob(os.path.join(*[dirPath, '*.png'])), key=natural_keys)
    imgs = []

    for i in tqdm(range(len(path_list))):
        img = Image.open(path_list[i])
        img = img.resize(size=(1600, 1200))
        imgs.append(img)

    print('Saving...')
    imgs[0].save(pathGif,
                 save_all=True, append_images=imgs[1:], optimize=False, duration=0.00001, loop=0)
    
if __name__ == '__main__':
    args = sys.argv
    createGif(args[1], args[2])