import pytest
import cv2
import service.colorSpaceService as colorSpaceService


img = cv2.imread('./img.jpg')
args = None


def test_getRGB():
    r, g, b = colorSpaceService.getRGB(img, args)
    _, _, _r = cv2.split(r)
    _, _g, _ = cv2.split(g)
    _b, _, _ = cv2.split(b)
    assert (img == cv2.merge([_b, _g, _r])).all()


def test_getHSV():
    h, s, v = colorSpaceService.getHSV(img, args)
    _h, _, _ = cv2.split(h)
    _, _s, _ = cv2.split(s)
    _, _, _v = cv2.split(v)
    assert (cv2.cvtColor(img, cv2.COLOR_BGR2HSV) == cv2.merge([_h, _s, _v])).all()


if __name__ == '__main__':
    pytest.main()
