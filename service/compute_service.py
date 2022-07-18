import cv2


def andOp(imgs, args):
    return imgs[0] & imgs[1]


def orOp(imgs, args):
    return imgs[0] | imgs[1]


def notOp(imgs, args):
    return ~imgs[0]


def add(imgs, args):
    return cv2.add(imgs[0], imgs[1])


def subtract(imgs, args):
    return cv2.subtract(imgs[0], imgs[1])


def multiply(imgs, args):
    return cv2.multiply(imgs[0], imgs[1])


def divide(imgs, args):
    return cv2.divide(imgs[0], imgs[1])
