# -*- coding: utf-8 -*- 
""" 
@File : histTest.py 
@Author: csc
@Date : 2022/7/18
"""
import cv2
import service.histService as histService

img = cv2.imread('./img.jpg')


def test_histCover():
    histogram = histService.histCover(img)
    cv2.imshow('hist', histogram)
    cv2.waitKey(0)