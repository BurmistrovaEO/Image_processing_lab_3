from PIL import Image, ImageDraw
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfilename
import os
import cv2
from pathlib import Path
import random
import time
import numpy as np
import statistics as stat
from image_slicer import slice, save_tiles


def file_open_general():
    f = askopenfilename(title="Select file", filetypes=(("jpg files", "*.jpg"), ("png files", "*.png"),
                                                        ("jpeg files", "*.jpeg")))
    if f:
        return Image.open(f)


def file_open_cv():
    f = askopenfilename(title="Select file", filetypes=(("jpg files", "*.jpg"), ("png files", "*.png"),
                                                        ("jpeg files", "*.jpeg")))
    if f:
        return cv2.imread(f, cv2.IMREAD_COLOR)


def file_save(im):
    f = asksaveasfile(mode='w', defaultextension=".png")
    if f:  # asksaveasfile return `None` if dialog closed with "cancel".
        abs_path = os.path.abspath(f.name)
        im.save(abs_path)
    f.close()


def split(im):
    fn = "blurred.png"
    imgLab = cv2.cvtColor(im, cv2.COLOR_BGR2LAB)
    blurred = cv2.GaussianBlur(imgLab, (5, 5), 0)
    imgLab = cv2.cvtColor(blurred, cv2.COLOR_LAB2RGB)
    blurred = Image.fromarray(imgLab)
    abs_path = os.path.abspath(fn)
    blurred.save(abs_path)
    tiles = slice("blurred.png", 4)
    #print(tiles[1])
    save_tiles(tiles, prefix='', directory="C:/Users/Kate/Pictures/slices_1", format='png')
    for tile in tiles:
        tmp = np.array(tile.image)
        red = []
        green = []
        blue = []
        print(np.shape(blue))
        np.append(blue, 6)
        print(np.shape(blue))
        for x in range(tmp.shape[0]):
            for y in range(tmp.shape[1]):
                (b, g, r) = tmp[x, y]
                #print(b, g, r)
                red.append(r)
                green.append(g)
                blue.append(b)
            std_dev_r = np.std(red)
            #print(red)
            std_dev_g = np.std(green)
            std_dev_b = np.std(blue)
            print(std_dev_r, std_dev_g, std_dev_b)




image = file_open_cv()
split(image)
