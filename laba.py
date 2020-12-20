from PIL import Image, ImageDraw
from PIL import ImageFilter
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfilename
import os
import cv2
import random
import time
import numpy as np
import statistics as stat

def file_save(im):
    f = asksaveasfile(mode='w', defaultextension=".jpg")
    if f:  # asksaveasfile return `None` if dialog closed with "cancel".
        abs_path = os.path.abspath(f.name)
        im.save(abs_path)
    f.close()


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


def split_and_merge(image):
    image = image.convert('HSV')
    st = Stack()
    n = Stack()
    a = []
    st.push([0, image.size[0], 0, image.size[1]])

    while st.size() > 0:
        a = st.pop()
        k = 0
        if a[1]-a[0] > 5 and a[3]-a[2] > 5:
            for x in range(a[0], a[1]-1):
                for y in range(a[2], a[3]-1):
                    hsv = image.load()
                    h = hsv[x, y][0]
                    s = hsv[x, y][1]
                    v = hsv[x, y][2]
                    h1 = hsv[x + 1, y][0]
                    s1 = hsv[x + 1, y][1]
                    v1 = hsv[x + 1, y][2]
                    h2 = hsv[x, y + 1][0]
                    s2 = hsv[x, y + 1][1]
                    v2 = hsv[x, y + 1][2]
                    if v1 - v >= 10 and v1 > v or v - v1 >= 10 and v > v1 or v2 - v >= 10 and v2 > v or v - v2 >= 10 and v > v2:
                        k = 1
                        break
        if k == 1:
            st.push([a[0], a[0] + (a[1] - a[0]) // 2, a[2], a[2] + (a[3] - a[2]) // 2])
            st.push([a[0] + (a[1] - a[0]) // 2, a[1], a[2], a[2] + (a[3] - a[2]) // 2])
            st.push([a[0], a[0] + (a[1] - a[0]) // 2, a[2] + (a[3] - a[2]) // 2, a[3]])
            st.push([a[0] + (a[1] - a[0]) // 2, a[1], a[2] + (a[3] - a[2]) // 2, a[3]])
        else:
            n.push([a[0], a[1], a[2], a[3]])

    while n.size() > 0:
        a = n.pop()
        sV = 0
        sH = 0
        sS = 0
        for x in range(a[0], a[1]):
            for y in range(a[2], a[3]):
                hsv = image.load()
                h = hsv[x, y][0]
                s = hsv[x, y][1]
                v = hsv[x, y][2]
                sH += h
                sV += v
                sS += s
        sH = sH // ((a[1] - a[0]) * (a[3] - a[2]))
        sV = sV // ((a[1] - a[0]) * (a[3] - a[2]))
        sS = sS // ((a[1] - a[0]) * (a[3] - a[2]))
        for x in range(a[0], a[1]):
            for y in range(a[2], a[3]):
                hsv = image.load()
                ImageDraw.Draw(image).point((x, y), (sH, sS, sV))
    image = image.convert('RGB')
    image.show()



img_1 = Image.open('C:/Users/Home/Desktop/pikuliak_merging.jpg')
b = split_and_merge(img_1)
