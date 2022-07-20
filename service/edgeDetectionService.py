import cv2
import numpy as np


def roberts(imgs, args=None):
    """
    Roberts 算子
    :return: img
    """
    img = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)
    kernelx = np.array([[-1, 0], [0, 1]], dtype=int)
    kernely = np.array([[0, -1], [1, 0]], dtype=int)

    x = cv2.filter2D(img, cv2.CV_16S, kernelx)
    y = cv2.filter2D(img, cv2.CV_16S, kernely)
    absX = cv2.convertScaleAbs(x)
    absY = cv2.convertScaleAbs(y)
    Roberts = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
    Roberts.astype('uint8')
    return Roberts


def sobel(imgs, args=None):
    """
    Sobel 算子
    :return: img
    """
    img = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)
    x = cv2.Sobel(img, cv2.CV_16S, 1, 0)
    y = cv2.Sobel(img, cv2.CV_16S, 0, 1)
    absX = cv2.convertScaleAbs(x)
    absY = cv2.convertScaleAbs(y)
    Sobel = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
    return Sobel


def laplacian(imgs, args):
    """
    Laplacian 算子
    blurSize: int | 高斯模糊 kernel 大小
    ksize: int | 算子大小
    :return: img
    """
    img = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (int(args['blurSize']), int(args['blurSize'])), 0)
    Laplacian = cv2.convertScaleAbs(cv2.Laplacian(img, cv2.CV_16S, ksize=int(args['ksize'])))
    return Laplacian


def LoG(imgs, args):
    """
    LoG 边缘算子
    blurSize: int | 高斯模糊 kernel 大小
    :return: img
    """
    bsize = int(args['blurSize'])
    img = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2RGB)
    img = cv2.copyMakeBorder(img, 2, 2, 2, 2, borderType=cv2.BORDER_REPLICATE)
    img = cv2.GaussianBlur(img, (bsize, bsize), 0, 0)
    m1 = np.array([[0, 0, -1, 0, 0],
                   [0, -1, -2, -1, 0],
                   [-1, -2, 16, -2, -1],
                   [0, -1, -2, -1, 0],
                   [0, 0, -1, 0, 0]])
    return cv2.filter2D(img, -1, m1)


def canny(imgs, args):
    """
    Canny 边缘检测
    blurSize: int | 高斯模糊 kernel 大小
    threshold1, threshold2: int, int | 低, 高阈值
    :return: img
    """
    bsize = int(args['blurSize'])
    blur = cv2.GaussianBlur(imgs[0], (bsize, bsize), 0)
    blur = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    gradx = cv2.Sobel(blur, cv2.CV_16SC1, 1, 0)
    grady = cv2.Sobel(blur, cv2.CV_16SC1, 0, 1)
    return cv2.Canny(gradx, grady, int(args['threshold1']), int(args['threshold2']))
