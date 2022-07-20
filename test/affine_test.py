# -*- coding: utf-8 -*- 
""" 
@File : affineTest.py 
@Author: csc
@Date : 2022/7/19
"""
import pytest

import cv2
import service.affineService as affineService
from main import display

img = cv2.imread('./img.jpg')
args = {
    'post1': [[50, 50], [200, 50], [50, 200]],
    'post2': [[10, 100], [200, 50], [100, 250]]
}


def test_Affine():
    res = affineService.affine([img], args)
    display('affine', res)
