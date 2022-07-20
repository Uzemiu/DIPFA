# -*- coding: utf-8 -*- 
""" 
@File : houghTest.py 
@Author: csc
@Date : 2022/7/19
"""
import cv2
import service.houghService as houghService

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
    cv2.imshow('hough', res)
    cv2.waitKey(0)


def test_houghP():
    res = houghService.houghP([img], args)
    cv2.imshow('houghP', res)
    cv2.waitKey(0)
