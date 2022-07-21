# -*- coding: utf-8 -*- 
""" 
@File : morphologyService.py 
@Author: csc
@Date : 2022/7/19
形态学操作
"""
import cv2
import numpy as np

structure = [cv2.MORPH_RECT, cv2.MORPH_CROSS, cv2.MORPH_ELLIPSE]


def erode(imgs, args):
    """
    腐蚀: 消除物体边界点，使目标缩小，可以消除小于结构元素的噪声点
    kernelType: int | 结构元类型 0: MORPH_RECT, 1: MORPH_CROSS, 2: MORPH_ELLIPSE
    kernelX, kernelY: int, int | (x, y) 结构元大小
    """
    kernel = cv2.getStructuringElement(structure[args['kernelType']],
                                       (int(args['kernelX']), int(args['kernelY'])))
    res = cv2.erode(imgs[0], kernel)
    return res


def dilate(imgs, args):
    """
    膨胀: 将与物体接触的所有背景点合并到物体中，使目标增大，可添补目标中的空洞
    kernelType: int | 结构元类型 0: MORPH_RECT, 1: MORPH_CROSS, 2: MORPH_ELLIPSE
    kernelSize: Tuple<int, int> | (x, y) 结构元大小
    """
    kernel = cv2.getStructuringElement(structure[int(args['kernelType'])],
                                       (int(args['kernelX']), int(args['kernelY'])))
    res = cv2.dilate(imgs[0], kernel)
    return res


def morphOpen(imgs, args):
    """
    开运算: 先腐蚀后膨胀，消除图像上细小的噪声，并平滑物体边界
    kernelType: int | 结构元类型 0: MORPH_RECT, 1: MORPH_CROSS, 2: MORPH_ELLIPSE
    kernelSize: Tuple<int, int> | (x, y) 结构元大小
    """
    kernel = cv2.getStructuringElement(structure[int(args['kernelType'])],
                                       (int(args['kernelX']), int(args['kernelY'])))
    res = cv2.morphologyEx(imgs[0], cv2.MORPH_OPEN, kernel)
    return res


def morphClose(imgs, args):
    """
    闭运算: 先膨胀后腐蚀，填充物体内细小的空洞，并平滑物体边界
    kernelType: int | 结构元类型 0: MORPH_RECT, 1: MORPH_CROSS, 2: MORPH_ELLIPSE
    kernelSize: Tuple<int, int> | (x, y) 结构元大小
    """
    kernel = cv2.getStructuringElement(structure[int(args['kernelType'])],
                                       (int(args['kernelX']), int(args['kernelY'])))
    res = cv2.morphologyEx(imgs[0], cv2.MORPH_CLOSE, kernel)
    return res
