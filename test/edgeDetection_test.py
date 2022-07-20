# -*- coding: utf-8 -*- 
""" 
@File : edgeDetectionTest.py 
@Author: csc
@Date : 2022/7/20
"""
import cv2
import service.edgeDetectionService as edgeDetectionService
from main import display

img = cv2.imread('./img.jpg')


def test_roberts():
    res = edgeDetectionService.roberts([img])
    display('Roberts', res)


def test_sobel():
    res = edgeDetectionService.sobel([img])
    display('Sobel', res)


def test_laplacian():
    res = edgeDetectionService.laplacian([img], {'blurSize': 3, 'ksize': 3})
    display('LoG', res)


def test_LoG():
    res = edgeDetectionService.LoG([img], {'blurSize': 3})
    display('LoG', res)


def test_canny():
    res = edgeDetectionService.canny([img], {'blurSize': 3, 'threshold1': 50, 'threshold2': 150})
    display('canny', res)
