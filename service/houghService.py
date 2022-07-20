# -*- coding: utf-8 -*- 
""" 
@File : houghService.py 
@Author: csc
@Date : 2022/7/19
霍夫变换
"""
import cv2
import numpy as np


def getEdges(img, bsize=3, threshold1=50, threshold2=150):
    """
    获取图像边缘
    """
    img = cv2.GaussianBlur(img, (bsize, bsize), 0)
    edges = cv2.Canny(img, threshold1=threshold1, threshold2=threshold2, apertureSize=3)
    return edges


def hough(imgs, args):
    """
    霍夫变换
    blurSize: 高斯噪声 kernel 大小
    cannyThreshold1, cannyThreshold2: canny 边缘检测阈值
    houghThreshold: hough 变换阈值
    """
    bsize = int(args['blurSize'])
    edges = getEdges(imgs[0], bsize, threshold1=int(args['cannyThreshold1']), threshold2=int(args['cannyThreshold2']))

    lines = cv2.HoughLines(edges, rho=1, theta=np.pi / 2, threshold=int(args['houghThreshold']))

    result = imgs[0].copy()
    for i_line in lines:
        for line in i_line:
            rho = line[0]
            theta = line[1]
            if theta < (np.pi / 4.0) or theta > (3. * np.pi / 4.0):  # 垂直直线
                pt1 = (int(rho / np.cos(theta)), 0)
                pt2 = (int((rho - result.shape[0] * np.sin(theta)) / np.cos(theta)), result.shape[0])
                cv2.line(result, pt1, pt2, (0, 0, 255))
            else:
                pt1 = (0, int(rho / np.sin(theta)))
                pt2 = (result.shape[1], int((rho - result.shape[1] * np.cos(theta)) / np.sin(theta)))
                cv2.line(result, pt1, pt2, (0, 0, 255))

    return result


def houghP(imgs, args):
    """
    概率霍夫变换
    blurSize: 高斯噪声 kernel 大小
    cannyThreshold1, cannyThreshold2: canny 边缘检测阈值
    houghThreshold: hough 变换阈值
    minLineLength: 可以组成一条直线的最小点数, 少于这个点数的直线被忽略。
    maxLineGap: 认为在同一直线上的两点之间的最大间隙。
    """
    bsize = int(args['blurSize'])
    edges = getEdges(imgs[0], bsize, threshold1=int(args['cannyThreshold1']), threshold2=int(args['cannyThreshold2']))

    linesP = cv2.HoughLinesP(edges, rho=1, theta=np.pi / 180, threshold=int(args['houghThreshold']),
                             minLineLength=int(args['minLineLength']), maxLineGap=int(args['maxLineGap']))

    result_P = imgs[0].copy()
    for i_P in linesP:
        for x1, y1, x2, y2 in i_P:
            cv2.line(result_P, (x1, y1), (x2, y2), (0, 0, 255))

    return result_P
