# -*- coding: utf-8 -*-
"""
@File : 123.py
@Author: csc
@Date : 2022/6/22
色彩空间
"""
import cv2
import numpy as np


def getRGB(img):
    """
    返回 RGB 三个通道对应的彩色图
    """
    b, g, r = cv2.split(img)
    zeros = np.zeros(img.shape[:2], dtype="uint8")
    return cv2.merge([zeros, zeros, r]), cv2.merge([zeros, g, zeros]), cv2.merge([b, zeros, zeros])


def getHSV(img):
    """
    返回 HSV 三个通道对应的彩色图
    """
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    zeros = np.zeros(img.shape[:2], dtype="uint8")
    # binary, full = cv2.threshold(zeros, -1, 255, cv2.THRESH_BINARY)
    return cv2.merge([h, zeros, zeros]), cv2.merge([zeros, s, zeros]), cv2.merge([zeros, zeros, v])
