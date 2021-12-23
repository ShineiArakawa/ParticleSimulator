import os 
import sys
import glob
import re
import cv2
from tqdm import tqdm

def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def createMP4(dirPath: str):
    path_list = sorted(
        glob.glob(os.path.join(*[dirPath, '*.png'])), key=natural_keys)
    print(path_list)

    # encoder(for mp4)
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    # output file name, encoder, fps, size(fit to image size)
    video = cv2.VideoWriter('video.mp4',fourcc, 60.0, (1600, 1200))

    if not video.isOpened():
        print("can't be opened")
        sys.exit()

    for i in tqdm(range(len(path_list))):
        img = cv2.imread(path_list[i])
        img = cv2.resize(img, (1600, 1200))

        # can't read image, escape
        if img is None:
            print("can't read")
            break

        # add
        video.write(img)

    video.release()
    print('written')
    
if __name__ == '__main__':
    args = sys.argv
    print('args= ', args)
    createMP4(args[1])