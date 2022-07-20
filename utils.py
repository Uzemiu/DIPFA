# -*- coding: utf-8 -*- 
""" 
@File : utils.py 
@Author: csc
@Date : 2022/7/18
"""
import numpy as np


def figure2ndarray(fig):
    """
    matplotlib.figure.Figure转为np.ndarray
    """
    fig.canvas.draw()
    w, h = fig.canvas.get_width_height()
    buf_ndarray = np.frombuffer(fig.canvas.tostring_rgb(), dtype='u1')
    img = buf_ndarray.reshape(h, w, 3)
    return img


def inArea(point: tuple, area: tuple):
    """
    点是否在区域内
    point: (x0, y0)
    area: ((x1, y1), (x2, y2)) 左上角 右下角
    """
    return area[0][0] <= point[0] <= area[1][0] and area[0][1] <= point[1] <= area[1][1]
