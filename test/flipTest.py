# -*- coding: utf-8 -*- 
""" 
@File : flipTest.py 
@Author: csc
@Date : 2022/7/18
"""
import cv2
import service.flipService as flipService

img = cv2.imread('./img.jpg')


def test_horizontalFlip():
    tmp = flipService.horizontalFlip([img])
    tmp = flipService.horizontalFlip([tmp])
    assert (img == tmp).all()


def test_verticalFlip():
    tmp = flipService.verticalFlip([img])
    tmp = flipService.verticalFlip([tmp])
    assert (img == tmp).all()
