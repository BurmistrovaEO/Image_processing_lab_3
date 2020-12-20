from PIL import Image, ImageDraw
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfilename
import os
from anytree import Node, RenderTree
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
    threshold = 6
    min_size = 400
    fn = "blurred.png"
    abs_path = os.path.abspath(fn)
    im.save(abs_path)
    tiles = slice("blurred.png", 4)
    #print(tiles[1])
    save_tiles(tiles, prefix='', directory="C:/Users/Kate/Pictures/slices_1", format='png')
    for tile in tiles:
        tmp = np.array(tile.image)
        value = []
        block = np.zeros((np.shape(tmp)))
        #print(np.shape(block))
        for x in range(tmp.shape[0]):
            for y in range(tmp.shape[1]):
                (h, s, v) = tmp[x, y]
                #print(b, g, r)
                value.append(v)
        mean = np.mean(value)
        for x in range(tmp.shape[0]):
            for y in range(tmp.shape[1]):
                (h, s, v) = tmp[x, y]
                if v - mean > threshold:
                    block[x, y] = 1
        #print(block)
        #print(mean)
        summa = 0
        for x in range(block.shape[0]):
            for y in range(block.shape[1]):
                summa += int(block[x][y][2])
        print(summa)
        xxy = int(block.shape[0]*block.shape[1])
        if summa != xxy and summa != 0 and xxy > min_size:
            split(tile)
        #print(block.shape[0]*block.shape[1])



image = file_open_cv()
imgLab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
blurred = cv2.GaussianBlur(imgLab, (5, 5), 0)
imgLab = cv2.cvtColor(blurred, cv2.COLOR_LAB2BGR)
imgHSV = cv2.cvtColor(imgLab, cv2.COLOR_BGR2HSV)
blurred = Image.fromarray(imgHSV)
split(blurred)
