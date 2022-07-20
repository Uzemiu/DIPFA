# -*- coding: utf-8 -*- 
""" 
@File : affineTest.py 
@Author: csc
@Date : 2022/7/19
"""
import json

import cv2
import service.affineService as affineService

img = cv2.imread('./img.jpg')
args = {
    'post1': [[50, 50], [200, 50], [50, 200]],
    'post2': [[10, 100], [200, 50], [100, 250]]
}


def test_Affine():
    res = affineService.affine([img], args)
    cv2.imshow('affine', res)
    cv2.waitKey(0)
