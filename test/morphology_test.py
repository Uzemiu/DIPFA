# -*- coding: utf-8 -*- 
""" 
@File : morphologyTest.py 
@Author: csc
@Date : 2022/7/19
"""
import cv2
import service.morphologyService as morphologyService
from main import display

img = cv2.imread('./img.jpg')
args = {
    'kernelType': 1,
    'kernelX': 3,
    'kernelY': 4
}


def test_erode():
    res = morphologyService.erode([img], args)
    display('erode', res)


def test_dilate():
    res = morphologyService.dilate([img], args)
    display('dilate', res)


def test_morphOpen():
    res = morphologyService.morphOpen([img], args)
    display('open', res)


def test_morphClose():
    res = morphologyService.morphClose([img], args)
    display('close', res)
