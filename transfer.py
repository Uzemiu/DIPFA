import cv2 as cv
import numpy as np
import argparse
import base64

# https://blog.csdn.net/WZZ18191171661/article/details/91048997
# https://zhuanlan.zhihu.com/p/50852257
# https://blog.csdn.net/u010751000/article/details/106163541

parser = argparse.ArgumentParser(
    description='This script is used to run style transfer models from '
                'https://github.com/jcjohnson/fast-neural-style using OpenCV')
parser.add_argument('--input', help='Path to image or video. Skip to capture frames from camera')
parser.add_argument('--model', help='Path to .t7 model')
parser.add_argument('--width', default=-1, type=int, help='Resize input to specific width.')
parser.add_argument('--height', default=-1, type=int, help='Resize input to specific height.')
parser.add_argument('--median_filter', default=0, type=int, help='Kernel size of postprocessing blurring.')


# args = parser.parse_args()

def get_model_file(model='candy'):
    return f'./models/{model}.t7'


def style_transfer(input, model, median_filter=0):
    net = cv.dnn.readNetFromTorch(get_model_file(model))

    frame = input
    inWidth = frame.shape[1]
    inHeight = frame.shape[0]
    inp = cv.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight),
                               (103.939, 116.779, 123.68), swapRB=False, crop=False)

    net.setInput(inp)
    out = net.forward()

    out = out.reshape(3, out.shape[2], out.shape[3])
    out[0] += 103.939
    out[1] += 116.779
    out[2] += 123.68
    out /= 255
    out = out.transpose(1, 2, 0)

    t, _ = net.getPerfProfile()
    freq = cv.getTickFrequency() / 1000
    print(t / freq, 'ms')

    if median_filter:
        out = cv.medianBlur(out, median_filter)

    return out * 255


if __name__ == '__main__':
    out = style_transfer('./images/z.jpg', 'the_wave')

    # base64 encode
    bimage = cv.imencode('.jpg', out)[1]
    base64_data = str(base64.b64encode(bimage))[2:-1]

    cv.namedWindow('Styled image', cv.WINDOW_NORMAL)
    cv.imwrite('./images/out.jpg', out)
    cv.imshow('Styled image', out / 255.0)
    cv.waitKey(-1)
