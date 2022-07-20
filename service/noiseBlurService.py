import cv2
import numpy as np


def sp_noise(imgs, args):
    """
    添加椒盐噪声
    svp: float | 盐噪声比例 0-1之间
    amount: float | 噪声占比 0-1之间
    :return: img
    """
    image = imgs[0]
    s_vs_p = float(args['svp'])
    # 设置添加噪声图像像素的数目
    amount = float(args['amount'])
    noisy_img = np.copy(image)
    # 添加salt噪声
    num_salt = np.ceil(amount * image.size * s_vs_p)
    # 设置添加噪声的坐标位置
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
    noisy_img[coords[0], coords[1], :] = [255, 255, 255]
    # 添加pepper噪声
    num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
    # 设置添加噪声的坐标位置
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
    noisy_img[coords[0], coords[1], :] = [0, 0, 0]
    return noisy_img


def gaussian_noise(imgs, args):
    """
    添加高斯噪声
    mean: float | 均值
    sigma: float | 标准差
    :return: img
    """
    # TODO 有问题
    image = imgs[0] / 255.0
    h, w, c = image.shape
    mean = float(args['mean'])
    sigma = float(args['sigma'])
    gauss = np.random.normal(mean, sigma, (h, w, c))
    noisy_img = image + gauss
    return np.clip(noisy_img, a_min=0, a_max=255)


def avg_blur(imgs, args):
    """
    算术均值滤波
    x, y: int, int | 滤波器大小
    :return: img
    """
    return cv2.blur(imgs[0], (int(args['x']), int(args['y'])))


def max_blur(imgs, args):
    """
    最大值滤波
    ksize: int | 滤波器大小
    :return: img
    """
    image = imgs[0]
    h, w, c = image.shape
    output = np.zeros(image.shape, np.uint8)
    ksize = int(args['ksize'])
    k2 = int(ksize / 2)
    for i in range(k2, h - k2):
        for j in range(k2, w - k2):
            for ch in range(c):
                output[i, j, ch] = np.max(image[i - k2:i + k2 + 1, j - k2:j + k2 + 1, ch])
    return output


def min_blur(imgs, args):
    """
    最小值滤波
    ksize: int | 滤波器大小
    :return: img
    """
    image = imgs[0]
    h, w, c = image.shape
    output = np.zeros(image.shape, np.uint8)
    ksize = int(args['ksize'])
    k2 = int(ksize / 2)
    for i in range(k2, h - k2):
        for j in range(k2, w - k2):
            for ch in range(c):
                output[i, j, ch] = np.min(image[i - k2:i + k2 + 1, j - k2:j + k2 + 1, ch])
    return output


def med_blur(imgs, args):
    """
    中值滤波
    ksize: 滤波器大小
    :return: img
    """
    return cv2.medianBlur(imgs[0], int(args['ksize']))


def gaussian_blur(imgs, args):
    """
    TODO
    """
    return cv2.GaussianBlur(imgs[0], (int(args['x']), int(args['y'])), 0)


def geometric_blur(imgs, args):
    """
    几何均值滤波
    ksize: int | 滤波器大小
    :return: img
    """
    kernel_size = int(args['ksize'])

    res = []
    for img in cv2.split(imgs[0]):
        G_mean_img = np.ones(img.shape)

        k = int((kernel_size - 1) / 2)

        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if i < k or i > (img.shape[0] - k - 1) or j < k or j > (img.shape[1] - k - 1):
                    G_mean_img[i][j] = img[i][j]
                else:
                    for n in range(kernel_size):
                        for m in range(kernel_size):
                            G_mean_img[i][j] *= np.float(img[i - k + n][j - k + m])
                    G_mean_img[i][j] = pow(G_mean_img[i][j], 1 / (kernel_size * kernel_size))

        G_mean_img = np.uint8(G_mean_img)
        res.append(G_mean_img)
    return cv2.merge(res)


def harmonic_blur(imgs, args):
    """
    谐波均值滤波
    ksize: int | 滤波器大小
    :return: img
    """
    kernel_size = int(args['ksize'])

    res = []
    for img in cv2.split(imgs[0]):
        H_mean_img = np.zeros(img.shape)

        k = int((kernel_size - 1) / 2)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if i < k or i > (img.shape[0] - k - 1) or j < k or j > (img.shape[1] - k - 1):
                    H_mean_img[i][j] = img[i][j]
                else:
                    for n in range(kernel_size):
                        for m in range(kernel_size):
                            if img[i - k + n][j - k + m] == 0:
                                H_mean_img[i][j] = 0
                                break
                            else:
                                H_mean_img[i][j] += 1 / np.float(img[i - k + n][j - k + m])
                        else:
                            continue
                        break

                    if H_mean_img[i][j] != 0:
                        H_mean_img[i][j] = (kernel_size * kernel_size) / H_mean_img[i][j]

        H_mean_img = np.uint8(H_mean_img)
        res.append(H_mean_img)
    return cv2.merge(res)


def low_pass_filter(imgs, args):
    """
    低通滤波
    threshold2: int | 阈值
    :return: img
    """
    threshold2 = int(args['threshold2'])
    image = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)
    output = np.zeros(image.shape, np.uint8)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if threshold2 > image[i][j]:
                output[i][j] = image[i][j]
            else:
                output[i][j] = 0

    return output


def high_pass_filter(imgs, args):
    """
    高通滤波
    threshold1: int | 阈值
    :return: img
    """
    threshold1 = int(args['threshold1'])
    image = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)
    output = np.zeros(image.shape, np.uint8)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if threshold1 < image[i][j]:
                output[i][j] = image[i][j]
            else:
                output[i][j] = 0

    return output


def band_pass_filter(imgs, args):
    """
    带通滤波
    threshold1, threshold2: int, int | 低阈值, 高阈值
    :return: img
    """
    threshold1 = int(args['threshold1'])
    threshold2 = int(args['threshold2'])
    image = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)
    output = np.zeros(image.shape, np.uint8)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if threshold1 < image[i][j] < threshold2:
                output[i][j] = image[i][j]
            else:
                output[i][j] = 0

    return output


def band_stop_filter(imgs, args):
    """
    带阻滤波
    threshold1, threshold2: int, int | 低阈值, 高阈值
    :return: img
    """
    threshold1 = int(args['threshold1'])
    threshold2 = int(args['threshold2'])
    image = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)
    output = np.zeros(image.shape, np.uint8)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if threshold1 < image[i][j] < threshold2:
                output[i][j] = 0
            else:
                output[i][j] = image[i][j]

    return output
