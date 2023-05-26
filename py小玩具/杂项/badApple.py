# -*- coding:utf-8 -*-
import time
import cv2
import numpy as np
from PIL import Image
import os
import curses

stdscr = curses.initscr()
stdscr.border(0)
codeLib = '''@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. '''  # 生成字符画所需的字符集
count = len(codeLib)


def main(video_path):
    '''
	对视频文件切割成帧
	@param video_path:视频路径
	'''
    vc = cv2.VideoCapture(video_path)
    c = 0
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False
    while rval:
        rval, frame = vc.read()
        # if c % 2 == 0:
        console_print(frame)
    # c=c+1


def transform(image_file):
    codePic = ''
    for row in range(0, image_file.shape[0]):  # size属性表示图片的分辨率，'0'为横向大小，'1'为纵向
        for col in range(0, image_file.shape[1]):
            r, g, b = image_file[row][col]
            gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)  # 返回指定位置的像素，如果所打开的图像是多层次的图片，那这个方法就返回一个元组
            codePic = codePic + codeLib[int(((count - 1) * gray) / 256)]  # 建立灰度与字符集的映射
        codePic = codePic + '\n'
    return codePic


def console_print(image_file):
    rows, cols, _ = image_file.shape
    image_file = cv2.resize(image_file, (int(cols * 0.25), int(rows * 0.12)))
    stdscr.addstr(0, 0, transform(image_file))
    stdscr.refresh()


main("badapple.mp4")
