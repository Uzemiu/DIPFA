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


def horizontalFlip(imgs, args=None):
    """
    水平翻转图像
    :return: img
    """
    return cv2.flip(imgs[0], HORIZONTAL)


def verticalFlip(imgs, args=None):
    """
    垂直翻转图像
    :return: img
    """
    return cv2.flip(imgs[0], VERTICAL)
