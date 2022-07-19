# -*- coding: utf-8 -*- 
""" 
@File : morphologyTest.py 
@Author: csc
@Date : 2022/7/19
"""
import cv2
import service.morphologyService as morphologyService

img = cv2.imread('./img.jpg')
args = {
    'kernelType': 'morph cross',
    'kernelSize': [3, 4]
}


def test_erode():
    res = morphologyService.erode(img, args)
    cv2.imshow('erode', res)
    cv2.waitKey(0)


def test_dilate():
    res = morphologyService.dilate(img, args)
    cv2.imshow('dilate', res)
    cv2.waitKey(0)


def test_morphOpen():
    res = morphologyService.morphOpen(img, args)
    cv2.imshow('open', res)
    cv2.waitKey(0)


def test_morphClose():
    res = morphologyService.morphClose(img, args)
    cv2.imshow('close', res)
    cv2.waitKey(0)
