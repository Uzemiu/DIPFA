import cv2
import numpy as np


def andOp(imgs, args=None):
    """
    与运算
    :return: img
    """
    return imgs[0] & imgs[1]


def orOp(imgs, args=None):
    """
    或运算
    :return: img
    """
    return imgs[0] | imgs[1]


def notOp(imgs, args=None):
    """
    非运算
    :return: img
    """
    return ~imgs[0]


def add(imgs, args=None):
    """
    加法运算
    :return: img
    """
    return cv2.add(imgs[0], imgs[1])


def subtract(imgs, args=None):
    """
    减法运算
    :return: img
    """
    return cv2.subtract(imgs[0], imgs[1])


def multiply(imgs, args=None):
    """
    乘法运算
    :return: img
    """
    return cv2.multiply(imgs[0], imgs[1])


def divide(imgs, args=None):
    """
    除法运算
    :return: img
    """
    return cv2.divide(imgs[0], imgs[1])


def scale(imgs, args):
    """
    缩放
    dstX, dstY: int, int | 目标大小
    :return: img
    """
    return cv2.resize(imgs[0], (int(args['xArg']), int(args['yArg'])), interpolation=cv2.INTER_LINEAR)


def translate(imgs, args):
    """
    平移
    xArg, yArg: float, float | x, y 方向上的平移距离
    :return: img
    """
    height, width, channel = imgs[0].shape
    M = np.float32([[1, 0, float(args['xArg'])], [0, 1, float(args['yArg'])]])
    return cv2.warpAffine(imgs[0], M, (width, height))


def rotate(imgs, args):
    """
    旋转
    x, y: int, int | 旋转中心
    deg: float | 旋转角度
    :return: img
    """
    height, width, channel = imgs[0].shape
    M = cv2.getRotationMatrix2D((int(args['x']), int(args['y'])), float(args['deg']), 1)
    return cv2.warpAffine(imgs[0], M, (width, height))
