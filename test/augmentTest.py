# -*- coding: utf-8 -*- 
""" 
@File : augmentTest.py 
@Author: csc
@Date : 2022/7/20
"""
import cv2
import service.augmentService as augmentService

img = cv2.imread('./img.jpg')


def test_lp_filter():
    res = augmentService.lp_filter([img], {'d0': 20, 'n': 2})
    cv2.imshow('lp_filter', res)
    cv2.waitKey(0)


def test_butterworth_lp_filter():
    res = augmentService.butterworth_lp_filter([img], {'d0': 20, 'n': 2})
    cv2.imshow('butterworth_lp_filter', res)
    cv2.waitKey(0)


def test_gauss_lp_filter():
    res = augmentService.gauss_lp_filter([img], {'d0': 20, 'n': 4})
    cv2.imshow('gauss_lp_filter', res)
    cv2.waitKey(0)


def test_hp_filter():
    res = augmentService.hp_filter([img], {'d0': 40, 'n': 2})
    cv2.imshow('hp_filter', res)
    cv2.waitKey(0)


def test_butterworth_hp_filter():
    res = augmentService.butterworth_hp_filter([img], {'d0': 40, 'n': 2})
    cv2.imshow('butterworth_hp_filter', res)
    cv2.waitKey(0)


def test_gauss_hp_filter():
    res = augmentService.gauss_hp_filter([img], {'d0': 40, 'n': 2})
    cv2.imshow('gauss_hp_filter', res)
    cv2.waitKey(0)


def test_roberts_grad():
    res = augmentService.roberts_grad([img])
    cv2.imshow('roberts_grad', res)
    cv2.waitKey(0)


def test_sobel_grad():
    res = augmentService.sobel_grad([img])
    cv2.imshow('sobel_grad', res)
    cv2.waitKey(0)


def test_prewitt_grad():
    res = augmentService.prewitt_grad([img])
    cv2.imshow('prewitt_grad', res)
    cv2.waitKey(0)


def test_laplacian_grad():
    res = augmentService.laplacian_grad([img])
    cv2.imshow('laplacian_grad', res)
    cv2.waitKey(0)
