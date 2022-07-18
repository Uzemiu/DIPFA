# -*- coding: utf-8 -*- 
""" 
@File : flipService.py 
@Author: csc
@Date : 2022/7/17
图像翻转
"""
import cv2

HORIZONTAL = 1
VERTICAL = 0


def horizontalFlip(img):
    """
    水平翻转图像
    """
    return cv2.flip(img, HORIZONTAL)


def verticalFlip(img):
    """
    垂直翻转图像
    """
    return cv2.flip(img, VERTICAL)
