# -*- coding: utf-8 -*- 
""" 
@File : noiseBlurTest.py 
@Author: csc
@Date : 2022/7/20
"""
import cv2
import service.noiseBlurService as noiseBlurService

img = cv2.imread('./img.jpg')
blur = noiseBlurService.sp_noise([img], {'svp': 0.5, 'amount': 0.01})


def test_sp_noise():
    res = noiseBlurService.sp_noise([img], {'svp': 0.5, 'amount': 0.1})
    cv2.imshow('sp_noise', res)
    cv2.waitKey(0)


def test_gaussian_noise():
    res = noiseBlurService.gaussian_noise([img], {'mean': 0.0, 'sigma': 25})
    cv2.imshow('gaussian_noise', res)
    cv2.waitKey(0)


def test_avg_blur():
    res = noiseBlurService.avg_blur([blur], {'x': 3, 'y': 3})
    cv2.imshow('avg_blur', res)
    cv2.waitKey(0)


def test_med_blur():
    res = noiseBlurService.med_blur([blur], {'ksize': 3})
    cv2.imshow('med_blur', res)
    cv2.waitKey(0)


def test_gaussian_blur():
    res = noiseBlurService.gaussian_blur([blur], {'x': 5, 'y': 5})
    cv2.imshow('gaussian_blur', res)
    cv2.waitKey(0)


def test_geometric_blur():
    res = noiseBlurService.geometric_blur([blur], {'ksize': 3})
    cv2.imshow('geometric_blur', res)
    cv2.waitKey(0)


def test_harmonic_blur():
    res = noiseBlurService.harmonic_blur([blur], {'ksize': 3})
    cv2.imshow('harmonic_blur', res)
    cv2.waitKey(0)


def test_low_pass_filter():
    res = noiseBlurService.low_pass_filter([blur], {'threshold2': 200})
    cv2.imshow('low_pass', res)
    cv2.waitKey(0)


def test_high_pass_filter():
    res = noiseBlurService.high_pass_filter([blur], {'threshold1': 100})
    cv2.imshow('high_pass', res)
    cv2.waitKey(0)


def test_band_pass_filter():
    res = noiseBlurService.band_pass_filter([blur], {'threshold1': 100, 'threshold2': 200})
    cv2.imshow('band_pass', res)
    cv2.waitKey(0)


def test_band_stop_filter():
    res = noiseBlurService.band_stop_filter([blur], {'threshold1': 100, 'threshold2': 200})
    cv2.imshow('band_stop', res)
    cv2.waitKey(0)
