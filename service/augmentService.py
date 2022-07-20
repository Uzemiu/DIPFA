import cv2
import numpy as np

import service.edgeDetectionService


def frequency_filter(image, filtered):
    fftImg = np.fft.fft2(image)  # 对图像进行傅里叶变换
    fftImgShift = np.fft.fftshift(fftImg)  # 傅里叶变换后坐标移动到图像中心
    handle_fftImgShift1 = fftImgShift * filtered  # 对傅里叶变换后的图像进行频域变换

    handle_fftImgShift2 = np.fft.ifftshift(handle_fftImgShift1)
    handle_fftImgShift3 = np.fft.ifft2(handle_fftImgShift2)
    handle_fftImgShift4 = np.real(handle_fftImgShift3)  # 傅里叶反变换后取频域
    return np.uint8(handle_fftImgShift4)


# 低通滤波
def lp_filter(imgs, args):
    """
    理想低通滤波
    d0: 截止频率
    """
    image = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)
    d0 = int(args['d0'])
    H = np.empty_like(image, dtype=float)
    M, N = image.shape
    mid_x = int(M / 2)
    mid_y = int(N / 2)
    for x in range(0, M):
        for y in range(0, N):
            d = np.sqrt((y - mid_x) ** 2 + (x - mid_y) ** 2)
            if d <= d0:
                H[x, y] = 1
    return frequency_filter(image, H)


def butterworth_lp_filter(imgs, args):
    """
    巴特沃斯低通滤波
    d0: 截止频率
    n: 阶数
    """
    image = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)
    d0 = int(args['d0'])
    n = int(args['n'])
    H = np.empty_like(image, float)
    M, N = image.shape
    mid_x = int(M / 2)
    mid_y = int(N / 2)
    for x in range(0, M):
        for y in range(0, N):
            d = np.sqrt((y - mid_x) ** 2 + (x - mid_y) ** 2)
            H[x, y] = 1 / (1 + (d / d0) ** (2 * n))
    return frequency_filter(image, H)


def gauss_lp_filter(imgs, args):
    """
    高斯低通滤波
    d0: 截止频率
    n: 阶数
    """
    image = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)
    d0 = int(args['d0'])
    n = int(args['n'])
    H = np.empty_like(image, float)
    M, N = image.shape
    mid_x = M / 2
    mid_y = N / 2
    for x in range(0, M):
        for y in range(0, N):
            d = np.sqrt((x - mid_x) ** 2 + (y - mid_y) ** 2)
            H[x, y] = np.exp(-d ** n / (2 * d0 ** n))
    return frequency_filter(image, H)


# 高通滤波
def hp_filter(imgs, args):
    """
    理想高通滤波
    d0: 截止频率
    """
    image = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)
    d0 = int(args['d0'])
    H = np.empty_like(image, dtype=float)
    M, N = image.shape
    mid_x = int(M / 2)
    mid_y = int(N / 2)
    for x in range(0, M):
        for y in range(0, N):
            d = np.sqrt((y - mid_x) ** 2 + (x - mid_y) ** 2)
            if d >= d0:
                H[x, y] = 1
    return frequency_filter(image, H)


def butterworth_hp_filter(imgs, args):
    """
    巴特沃斯高通滤波
    d0: 截止频率
    n: 阶数
    """
    image = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)
    d0 = int(args['d0'])
    n = int(args['n'])
    H = np.empty_like(image, float)
    M, N = image.shape
    mid_x = int(M / 2)
    mid_y = int(N / 2)
    for x in range(0, M):
        for y in range(0, N):
            d = np.sqrt((y - mid_x) ** 2 + (x - mid_y) ** 2)
            H[x, y] = 1 / (1 + (d0 / d) ** n)
    return frequency_filter(image, H)


def gauss_hp_filter(imgs, args):
    """
    高斯高通滤波
    d0: 截止频率
    n: 阶数
    """
    image = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)
    d0 = int(args['d0'])
    n = int(args['n'])
    H = np.empty_like(image, float)
    M, N = image.shape
    mid_x = M / 2
    mid_y = N / 2
    for x in range(0, M):
        for y in range(0, N):
            d = np.sqrt((x - mid_x) ** 2 + (y - mid_y) ** 2)
            H[x, y] = (1 - np.exp(-d ** n / (2 * d0 ** n)))
    return frequency_filter(image, H)


def roberts_grad(imgs, args=None):
    """
    Roberts 梯度算子
    """
    return service.edgeDetectionService.roberts(imgs, args)


def sobel_grad(imgs, args=None):
    """
    Sobel 梯度算子
    """
    return service.edgeDetectionService.sobel(imgs, args)


def prewitt_grad(imgs, args=None):
    """
    Prewitt梯度算子
    """
    image = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)
    preX = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
    preY = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
    x = cv2.filter2D(image, cv2.CV_16S, preX)
    y = cv2.filter2D(image, cv2.CV_16S, preY)

    absX = cv2.convertScaleAbs(x)
    absY = cv2.convertScaleAbs(y)
    return cv2.addWeighted(absX, 0.5, absY, 0.5, 0)


def laplacian_grad(imgs, args=None):
    """
    Laplacian梯度算子
    """
    image = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)
    lap = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
    return cv2.filter2D(image, ddepth=-1, kernel=lap)
