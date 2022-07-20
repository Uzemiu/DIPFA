# -*- coding: utf-8 -*- 
""" 
@File : computeTest.py 
@Author: csc
@Date : 2022/7/20
"""
import cv2
import numpy as np

from service.computeService import *


img = cv2.imread('./img.jpg')
img0 = np.zeros_like(img)
img255 = np.full_like(img, 255)
img100 = np.full_like(img, 100)
img200 = np.full_like(img, 200)


def test_addOp():
    assert (img0 == andOp([img, img0])).all()
    assert (img == andOp([img, img255])).all()


def test_orOp():
    assert (img == orOp([img, img0])).all()
    assert (img255 == orOp([img, img255])).all()


def test_notOp():
    assert (img0 == notOp([notOp([img0])])).all()


def test_add():
    assert (img200 == add([img100, img100])).all()
    assert (img255 == add([img100, img200])).all()


def test_subtract():
    assert (img100 == subtract([img200, img100])).all()


def test_multiply():
    assert (img0 == multiply([img0, img])).all()


def test_divide():
    assert (img0 == divide([img0, img])).all()


def test_scale():
    height, width, channel = img.shape
    res = scale([img], {'dstX': width / 2, 'dstY': height / 2})
    cv2.imshow('scale', res)
    cv2.waitKey(0)


def test_translate():
    res = translate([img], {'xArg': 10, 'yArg': 10})
    cv2.imshow('translate', res)
    cv2.waitKey(0)


def test_rotate():
    height, width, channel = img.shape
    res = rotate([img], {'x': height / 2, 'y': width / 2, 'deg': 90})
    cv2.imshow('rotate', res)
    cv2.waitKey(0)
