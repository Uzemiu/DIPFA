import json
import os
import traceback
import uuid

import numpy as np
import cv2 as cv

import transfer
import service.computeService as compute_service
import service.edgeDetectionService as edge_detection_service
import service.noiseBlurService as noise_blur_service
import service.augmentService as augment_service

from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS, cross_origin
import base64

app = Flask(__name__, static_folder='static', static_url_path='/')
cors = CORS(app)


def base64_encode(img):
    return str(base64.b64encode(cv.imencode('.jpg', img)[1]))[2:-1]


def base_response(status=200, message='ok', data=None):
    return {
        'status': status,
        'message': message,
        'data': data
    }


def style_transfer(images, args):
    return transfer.style_transfer(images[0], args['model'])


command_map = {
    # 基本计算
    'and': compute_service.andOp,
    'or': compute_service.orOp,
    'not': compute_service.notOp,
    'add': compute_service.add,
    'subtract': compute_service.subtract,
    'multiply': compute_service.multiply,
    'divide': compute_service.divide,
    'scale': compute_service.scale,
    'translate': compute_service.translate,
    'rotate': compute_service.rotate,
    # 边缘检测
    'roberts': edge_detection_service.roberts,
    'sobel': edge_detection_service.sobel,
    'laplacian': edge_detection_service.laplacian,
    'LoG': edge_detection_service.LoG,
    'canny': edge_detection_service.canny,
    # 噪声滤波,
    # 添加噪声
    'spNoise': noise_blur_service.sp_noise,
    'gaussianNoise': noise_blur_service.gaussian_noise,
    # 均值/排序统计滤波
    'avgBlur': noise_blur_service.avg_blur,
    'maxBlur': noise_blur_service.max_blur,
    'minBlur': noise_blur_service.min_blur,
    'medBlur': noise_blur_service.med_blur,
    'gaussianBlur': noise_blur_service.gaussian_blur,
    'geometricBlur': noise_blur_service.geometric_blur,
    'harmonicBlur': noise_blur_service.harmonic_blur,
    # 选择性滤波
    'lowPass': noise_blur_service.low_pass_filter,
    'highPass': noise_blur_service.high_pass_filter,
    'bandPass': noise_blur_service.band_pass_filter,
    'bandStop': noise_blur_service.band_stop_filter,
    # 图像增强
    'lpFilter': augment_service.lp_filter,
    'blpFilter': augment_service.butterworth_lp_filter,
    'glpFilter': augment_service.gauss_lp_filter,
    'hpFilter': augment_service.hp_filter,
    'bhpFilter': augment_service.butterworth_hp_filter,
    'ghpFilter': augment_service.gauss_hp_filter,
    'robertsGrad': augment_service.roberts_grad,
    'sobelGrad': augment_service.sobel_grad,
    'prewittGrad': augment_service.prewitt_grad,
    'laplacianGrad': augment_service.laplacian_grad,

    # 风格迁移
    'transfer': style_transfer,
}


@app.errorhandler(Exception)
def exception_handler(e):
    msg = e.args[0] if e.args[0] else 'Internal server error'
    traceback.print_exc()
    return jsonify(base_response(400, msg)), 400  # 一般异常


@app.route('/')
def index():  # put application's code here
    return send_file('./static/index.html')


@app.route('/process', methods=['POST'])
def upload():
    # parse form data
    command = request.form.get('command')
    files = request.files.getlist('files')
    dst = []
    for file in files:
        dst.append('./images/' + str(uuid.uuid1()))

    args = {}
    try:
        args = json.loads(request.form['args'])
    except:
        print(f'error in parse json: {args}')

    # execute command
    do_command = command_map.get(command)
    if do_command:
        try:
            for i in range(len(files)):
                files[i].save(dst[i])
            imgs = []
            for d in dst:
                imgs.append(cv.imread(d, 1))
            resp_data = do_command(imgs, args)
            resp_data = base64_encode(resp_data)
        except Exception as e:
            raise e
        finally:
            # clean tmp file
            for path in dst:
                os.remove(path)
    else:
        raise Exception(f'未知命令: {command}')

    return jsonify(base_response(data=resp_data))


if __name__ == '__main__':
    app.run()
