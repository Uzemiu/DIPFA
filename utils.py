# -*- coding: utf-8 -*- 
""" 
@File : utils.py 
@Author: csc
@Date : 2022/7/18
"""
import numpy as np
import torch
import torchvision.transforms as transforms


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


cnn_normalization_mean = [0.485, 0.456, 0.406]
cnn_normalization_std = [0.229, 0.224, 0.225]
tensor_normalizer = transforms.Normalize(mean=cnn_normalization_mean, std=cnn_normalization_std)
epsilon = 1e-5

def mean_std(features):
    """输入 VGG19 计算的四个特征，输出每张特征图的均值和标准差，长度为1920"""
    mean_std_features = []
    for x in features:
        x = x.view(*x.shape[:2], -1)
        x = torch.cat([x.mean(-1), torch.sqrt(x.var(-1) + epsilon)], dim=-1)
        n = x.shape[0]
        x2 = x.view(n, 2, -1).transpose(2, 1).contiguous().view(n, -1)  # [mean, ..., std, ...] to [mean, std, ...]
        mean_std_features.append(x2)
    mean_std_features = torch.cat(mean_std_features, dim=-1)
    return mean_std_features
