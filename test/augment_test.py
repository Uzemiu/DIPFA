# -*- coding: utf-8 -*- 
""" 
@File : augmentTest.py 
@Author: csc
@Date : 2022/7/20
"""
import cv2
import service.augmentService as augmentService
from main import display

img = cv2.imread('./img.jpg')


def test_lp_filter():
    res = augmentService.lp_filter([img], {'d0': 20, 'n': 2})
    display('lp_filter', res)


def test_butterworth_lp_filter():
    res = augmentService.butterworth_lp_filter([img], {'d0': 20, 'n': 2})
    display('butterworth_lp_filter', res)


def test_gauss_lp_filter():
    res = augmentService.gauss_lp_filter([img], {'d0': 20, 'n': 4})
    display('gauss_lp_filter', res)


def test_hp_filter():
    res = augmentService.hp_filter([img], {'d0': 40, 'n': 2})
    display('hp_filter', res)


def test_butterworth_hp_filter():
    res = augmentService.butterworth_hp_filter([img], {'d0': 40, 'n': 2})
    display('butterworth_hp_filter', res)


def test_gauss_hp_filter():
    res = augmentService.gauss_hp_filter([img], {'d0': 40, 'n': 2})
    display('gauss_hp_filter', res)


def test_roberts_grad():
    res = augmentService.roberts_grad([img])
    display('roberts_grad', res)


def test_sobel_grad():
    res = augmentService.sobel_grad([img])
    display('sobel_grad', res)


def test_prewitt_grad():
    res = augmentService.prewitt_grad([img])
    display('prewitt_grad', res)


def test_laplacian_grad():
    res = augmentService.laplacian_grad([img])
    display('laplacian_grad', res)
