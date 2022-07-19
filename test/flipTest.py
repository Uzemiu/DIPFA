# -*- coding: utf-8 -*- 
""" 
@File : flipTest.py 
@Author: csc
@Date : 2022/7/18
"""
import cv2
import service.flipService as flipService

img = cv2.imread('./img.jpg')
args = None


def test_horizontalFlip():
    tmp = flipService.horizontalFlip(img, args)
    tmp = flipService.horizontalFlip(tmp, args)
    assert (img == tmp).all()


def test_verticalFlip():
    tmp = flipService.verticalFlip(img, args)
    tmp = flipService.verticalFlip(tmp, args)
    assert (img == tmp).all()
