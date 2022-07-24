# -*- coding: utf-8 -*- 
""" 
@File : genCOCO2014_1000.py 
@Author: csc
@Date : 2022/7/24
"""
import os
import shutil
import numpy as np


def move_file(src, dst, num=None, type='move'):
    path_main = src
    filelist_main = os.listdir(src)
    filelist_main = np.array(filelist_main)
    if num is None:
        num = len(filelist_main)
    else:
        np.random.seed(42)
        np.random.shuffle(filelist_main)

    path_receive = dst

    for i in range(num):
        file = filelist_main[i]
        suffix = os.path.splitext(file)[1]  # 读取文件后缀名
        filename = os.path.splitext(file)[0]  # 读取文件名
        if suffix == '.jpg':
            src_path = os.path.join(path_main, file)
            dst_path = path_receive + '\\' + file
            if type == 'move':
                shutil.move(src_path, dst_path)
            elif type == 'copy':
                shutil.copy(src_path, dst_path)


if __name__ == '__main__':
    src = "../../COCO2014/train2014"
    content_path = "./COCO2014_1000/"
    content_class = "train2014"
    try:
        shutil.rmtree(content_path + content_class)
    except:
        os.mkdir(content_path)
    os.mkdir(content_path + content_class)
    move_file(src, content_path + content_class, num=1000, type='copy')
