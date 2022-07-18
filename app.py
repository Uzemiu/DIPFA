import json
import os
import traceback
import uuid

import numpy as np
import cv2 as cv

import transfer
import service.compute_service as compute_service

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
    'and': compute_service.andOp,
    'or': compute_service.orOp,
    'not': compute_service.notOp,
    'add': compute_service.add,
    'subtract': compute_service.subtract,
    'multiply': compute_service.multiply,
    'divide': compute_service.divide,
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
