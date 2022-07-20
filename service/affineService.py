# -*- coding: utf-8 -*- 
""" 
@File : affineService.py 
@Author: csc
@Date : 2022/7/19
仿射变换
"""
import cv2
import numpy as np
import utils


def affine(imgs, args):
    """
    仿射变化
    post1: [[x1, y1], [x2, y2], [x3, y3]]  三个点
    post2: [[x1, y1], [x2, y2], [x3, y3]]  三个点
    """
    rows, cols, channel = imgs[0].shape
    for point in args['post1'] + args['post2']:
        if not utils.inArea(point, ((0, 0), (rows, cols))):
            raise Exception(f'affine: point {str(point)} lies outside the image.')

    post1 = np.float32(args['post1'])
    post2 = np.float32(args['post2'])
    M = cv2.getAffineTransform(post1, post2)

    res = cv2.warpAffine(imgs[0], M, (rows, cols))
    return res
