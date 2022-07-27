# -*- coding: utf-8 -*- 
""" 
@File : noiseBlurTest.py 
@Author: csc
@Date : 2022/7/20
"""
import cv2
import service.noiseBlurService as noiseBlurService
from main import display

img = cv2.imread('./img.jpg')
blur = noiseBlurService.sp_noise([img], {'svp': 0.5, 'amount': 0.01})


def test_sp_noise():
    res = noiseBlurService.sp_noise([img], {'svp': 0.5, 'amount': 0.1})
    display('sp_noise', res)


# 有问题，但前端正常
def test_gaussian_noise():
    res = noiseBlurService.gaussian_noise([img], {'mean': 0.0, 'sigma': 25})
    display('gaussian_noise', res)


def test_avg_blur():
    res = noiseBlurService.avg_blur([blur], {'x': 3, 'y': 3})
    display('avg_blur', res)


def test_max_blur():
    res = noiseBlurService.max_blur([blur], {'ksize': 3})
    display('max_blur', res)


def test_min_blur():
    res = noiseBlurService.min_blur([blur], {'ksize': 3})
    display('min_blur', res)


def test_med_blur():
    res = noiseBlurService.med_blur([blur], {'ksize': 3})
    display('med_blur', res)


def test_gaussian_blur():
    res = noiseBlurService.gaussian_blur([blur], {'x': 3, 'y': 3})
    display('gaussian_blur', res)


def test_geometric_blur():
    res = noiseBlurService.geometric_blur([blur], {'ksize': 3})
    display('geometric_blur', res)


def test_harmonic_blur():
    res = noiseBlurService.harmonic_blur([blur], {'ksize': 3})
    display('harmonic_blur', res)


def test_low_pass_filter():
    res = noiseBlurService.low_pass_filter([blur], {'threshold2': 200})
    display('low_pass', res)


def test_high_pass_filter():
    res = noiseBlurService.high_pass_filter([blur], {'threshold1': 100})
    display('high_pass', res)


def test_band_pass_filter():
    res = noiseBlurService.band_pass_filter([blur], {'threshold1': 100, 'threshold2': 200})
    display('band_pass', res)


def test_band_stop_filter():
    res = noiseBlurService.band_stop_filter([blur], {'threshold1': 100, 'threshold2': 200})
    display('band_stop', res)
