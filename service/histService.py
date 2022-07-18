# -*- coding: utf-8 -*- 
""" 
@File : histService.py 
@Author: csc
@Date : 2022/7/18
直方图
"""
import cv2
import matplotlib.pyplot as plt
from utils import figure2ndarray


def histCover(img):
    """
    获取 img 的直方图
    返回一张有三条折线的直方图
    """
    color = ['r', 'g', 'b']
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    fig = plt.figure()
    for index, c in enumerate(color):
        hist = cv2.calcHist([img], [index], None, [256], [0, 255])
        plt.plot(hist, color=c)
        plt.xlim([0, 255])

    return figure2ndarray(fig)
