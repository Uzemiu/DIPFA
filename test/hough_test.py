# -*- coding: utf-8 -*- 
""" 
@File : houghTest.py 
@Author: csc
@Date : 2022/7/19
"""
import cv2
import service.houghService as houghService
from main import display

img = cv2.imread('./hough.png')
args = {
    'blurSize': 3,
    'cannyThreshold1': 50,
    'cannyThreshold2': 150,
    'houghThreshold': 118,
    'houghPThreshold': 118,
    'minLineLength': 200,
    'maxLineGap': 30
}


def test_hough():
    res = houghService.hough([img], args)
    display('hough', res)


def test_houghP():
    res = houghService.houghP([img], args)
    display('houghP', res)
