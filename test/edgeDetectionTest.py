# -*- coding: utf-8 -*- 
""" 
@File : edgeDetectionTest.py 
@Author: csc
@Date : 2022/7/20
"""
import cv2
import service.edgeDetectionService as edgeDetectionService

img = cv2.imread('./img.jpg')


def test_roberts():
    res = edgeDetectionService.roberts([img])
    cv2.imshow('Roberts', res)
    cv2.waitKey(0)


def test_sobel():
    res = edgeDetectionService.sobel([img])
    cv2.imshow('Sobel', res)
    cv2.waitKey(0)


def test_laplacian():
    res = edgeDetectionService.laplacian([img], {'blurSize': 3, 'ksize': 3})
    cv2.imshow('LoG', res)
    cv2.waitKey(0)


def test_LoG():
    res = edgeDetectionService.LoG([img], {'blurSize': 3})
    cv2.imshow('LoG', res)
    cv2.waitKey(0)


def test_canny():
    res = edgeDetectionService.canny([img], {'blurSize': 3, 'threshold1': 50, 'threshold2': 150})
    cv2.imshow('canny', res)
    cv2.waitKey(0)
