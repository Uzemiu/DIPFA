# -*- coding: utf-8 -*- 
""" 
@File : histTest.py 
@Author: csc
@Date : 2022/7/18
"""
import cv2
import service.histService as histService
from main import display

img = cv2.imread('./img.jpg')


def test_histCover():
    histogram = histService.histCover([img])
    display('hist', histogram)
