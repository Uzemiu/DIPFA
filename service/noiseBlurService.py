import cv2
import numpy as np


def sp_noise(imgs, args):
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
    image = imgs[0]
    h, w, c = image.shape
    mean = int(args['mean'])
    sigma = int(args['sigma'])
    gauss = np.random.normal(mean, sigma, (h, w, c))
    noisy_img = image + gauss
    return np.clip(noisy_img, a_min=0, a_max=255)


def avg_blur(imgs, args):
    return cv2.blur(imgs[0], (int(args['x']), int(args['y'])))


def med_blur(imgs, args):
    return cv2.medianBlur(imgs[0], int(args['ksize']))


def gaussian_blur(imgs, args):
    return cv2.GaussianBlur(imgs[0], (int(args['x']), int(args['y'])), 0)


def geometric_blur(imgs, args):
    kernel_size = int(args['ksize'])
    img = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)
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
    return G_mean_img


def harmonic_blur(imgs, args):
    kernel_size = int(args['ksize'])
    img = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)
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
    return H_mean_img


def low_pass_filter(imgs, args):
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
