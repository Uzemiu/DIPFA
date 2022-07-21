# -*- coding: utf-8 -*- 
""" 
@File : main.py.py 
@Author: csc
@Date : 2022/7/20
"""
import pytest
import cv2

show_img = True


def display(name: str, img) -> None:
    if show_img:
        cv2.imshow(name, img)
        cv2.waitKey(0)
        try:
            cv2.destroyWindow(name)
        except Exception:
            pass


if __name__ == '__main__':
    pytest.main()
