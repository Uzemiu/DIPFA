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
