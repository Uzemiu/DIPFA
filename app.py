import json
import os
import traceback
import uuid

import numpy as np
import cv2 as cv

import transfer

from flask import Flask, request, jsonify, render_template
import base64

app = Flask(__name__, static_folder='static', static_url_path='/')

def base64_encode(img):
    return str(base64.b64encode(cv.imencode('.jpg', img)[1]))[2:-1]

def base_response(status=200, message='ok', data=None):
    return {
        'status': status,
        'message': message,
        'data': data
    }


def style_transfer(image, args):
    return transfer.style_transfer(image, args['model'])


def new_operation(image, args):
    print('do something with the image')


command_map = {
    'transfer': style_transfer,
}


@app.errorhandler(Exception)
def exception_handler(e):
    msg = e.args[0] if e.args[0] else 'Internal server error'
    traceback.print_exc()
    return jsonify(base_response(400, msg)), 400  # 一般异常


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def upload():
    # parse form data
    command = request.form['command']
    file = request.files['file']
    dst = './images/' + str(uuid.uuid1())

    args = {}
    try:
        args = json.loads(request.form['args'])
    except:
        print(f'error in parse json: {args}')

    # execute command
    do_command = command_map.get(command)
    if do_command:
        try:
            file.save(dst)
            resp_data = do_command(dst, args)
            resp_data = base64_encode(resp_data)
        except Exception as e:
            raise e
        finally:
            # clean tmp file
            os.remove(dst)
    else:
        raise Exception(f'unknown command: {command}')

    return jsonify(base_response(data=resp_data))


if __name__ == '__main__':
    app.run()