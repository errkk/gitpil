from tester import *

from PIL import Image
from PIL import ImageChops

def test_offset():
    
    im1 = lena()

    assert_exception(AttributeError, lambda: im1.offset(10))

    im2 = ImageChops.offset(im1, 10)
    assert_equal(im1.getpixel((0, 0)), im2.getpixel((10, 10)))

    im2 = ImageChops.offset(im1, 10, 20)
    assert_equal(im1.getpixel((0, 0)), im2.getpixel((10, 20)))

    im2 = ImageChops.offset(im1, 20, 20)
    assert_equal(im1.getpixel((0, 0)), im2.getpixel((20, 20)))
